from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.db.models import Sum
from apps.donations.models import Donation

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'phone', 
            'password', 'confirm_password', 'profile_picture'
        ]
        extra_kwargs = {
            'password': {'write_only': True, 'style': {'input_type': 'password'}},
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        validate_password(attrs['password'])
        
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        return user
    
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        
        data['user'] = {
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'email': self.user.email,
            'profile_picture': self.user.profile_picture.url if self.user.profile_picture else None,
        }
        return data

class UserProfileSerializer(serializers.ModelSerializer):
    # 1. Define the custom read-only fields matching the React frontend
    projectsSupported = serializers.SerializerMethodField()
    totalContribution = serializers.SerializerMethodField()
    impactLevel = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'first_name', 'last_name', 'email', 'phone', 
            'profile_picture', 'birthdate', 'facebook_profile', 'country',
            'projectsSupported', 'totalContribution', 'impactLevel' # <-- Add them here
        ]
        read_only_fields = ['email']

    # 2. Logic to count unique projects supported
    def get_projectsSupported(self, obj):
        try:
            # Note: If your team named the foreign key 'donor' instead of 'user', 
            # simply change `user=obj` to `donor=obj` below.
            return Donation.objects.filter(user=obj).values('project').distinct().count()
        except Exception:
            return 0

    # 3. Logic to sum the total money donated
    def get_totalContribution(self, obj):
        try:
            total = Donation.objects.filter(user=obj).aggregate(total_sum=Sum('amount'))['total_sum']
            return total if total is not None else 0
        except Exception:
            return 0

    # 4. Logic to determine Impact Level based on total
    def get_impactLevel(self, obj):
        total = self.get_totalContribution(obj)
        
        if total >= 50000:
            return "Visionary"
        elif total >= 10000:
            return "Champion"
        elif total > 0:
            return "Supporter"
        
        return "Newcomer"


class DeleteAccountSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    def validate_password(self, value):
        user = self.context['request'].user
        
        if not user.check_password(value):
            # Increment the counter
            user.failed_delete_attempts += 1
            user.save(update_fields=['failed_delete_attempts'])
            
            # If they hit 10 attempts, trigger the lockout
            if user.failed_delete_attempts >= 10:
                raise serializers.ValidationError({"action": "terminate_session"})
                
            raise serializers.ValidationError("Incorrect password. Account deletion failed.")
        
        # If password is correct, reset the counter
        if user.failed_delete_attempts > 0:
            user.failed_delete_attempts = 0
            user.save(update_fields=['failed_delete_attempts'])
            
        return value