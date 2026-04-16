from rest_framework import serializers
from .models import Rating
from apps.accounts.models import User

class RatingSerializer(serializers.ModelSerializer):
   class Meta:
      model = Rating
      fields=['value']

   def validate_value(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating value must be between 1 and 5.")
        return value

   def validate(self, attrs):
       request=self.context.get('request')
       project=self.context.get('project')

       if project.owner == request.user:
           raise serializers.ValidationError("You cannot rate your own project.")
       if not self.instance:
         if Rating.objects.filter(project=project, user=request.user).exists():
            raise serializers.ValidationError("You have already rated this project.")
       return attrs
   
class UserMiniSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['email', 'full_name', 'profile_picture']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

class RatingListSerializer(serializers.ModelSerializer):
    user = UserMiniSerializer(read_only=True)

    class Meta:
        model = Rating
        fields = ['id', 'user', 'value', 'created_at']