from rest_framework import serializers
from .models import Project, ProjectPicture, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class ProjectPictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectPicture
        fields = ['id', 'image']


class ProjectSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    pictures = ProjectPictureSerializer(many=True, read_only=True)

    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        write_only=True,
        required=False,
        source='tags',
    )
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False,
    )

    total_donated = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    donation_percentage = serializers.FloatField(read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    owner = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Project
        fields = [
            'id', 'title', 'details', 'category',
            'total_target', 'start_time', 'end_time',
            'status', 'is_featured', 'owner',
            'tags', 'tag_ids',
            'pictures', 'uploaded_images',
            'total_donated', 'donation_percentage', 'average_rating',
            'created_at',
        ]
        read_only_fields = ['status', 'is_featured', 'owner', 'created_at']

    def validate(self, attrs):
        start = attrs.get('start_time')
        end = attrs.get('end_time')
        if start and end and end <= start:
            raise serializers.ValidationError({'end_time': 'End time must be after start time.'})
        return attrs

    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        images = validated_data.pop('uploaded_images', [])

        project = Project.objects.create(**validated_data)
        project.tags.set(tags)

        for img in images:
            ProjectPicture.objects.create(project=project, image=img)

        return project

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', None)
        images = validated_data.pop('uploaded_images', [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if tags is not None:
            instance.tags.set(tags)

        for img in images:
            ProjectPicture.objects.create(project=instance, image=img)

        return instance
