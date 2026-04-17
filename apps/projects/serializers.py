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

    tag_names = serializers.ListField(
        child=serializers.CharField(max_length=50),
        write_only=True,
        required=False,
    )
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False,
    )

    total_donated = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    donation_percentage = serializers.FloatField(read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    owner = serializers.SerializerMethodField(read_only=True)
    owner_id = serializers.IntegerField(source='owner.id', read_only=True)

    def get_owner(self, obj):
        return f"{obj.owner.first_name} {obj.owner.last_name}".strip() or obj.owner.email

    class Meta:
        model = Project
        fields = [
            'id', 'title', 'details', 'category',
            'total_target', 'start_time', 'end_time',
            'status', 'is_featured', 'owner', 'owner_id',
            'tags', 'tag_names',
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

    def _resolve_tags(self, names: list) -> list:
        return [Tag.objects.get_or_create(name=n.strip().lower())[0] for n in names if n.strip()]

    def create(self, validated_data):
        tag_names = validated_data.pop('tag_names', [])
        images = validated_data.pop('uploaded_images', [])

        project = Project.objects.create(**validated_data)
        project.tags.set(self._resolve_tags(tag_names))

        for img in images:
            ProjectPicture.objects.create(project=project, image=img)

        return project

    def update(self, instance, validated_data):
        tag_names = validated_data.pop('tag_names', None)
        images = validated_data.pop('uploaded_images', [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if tag_names is not None:
            instance.tags.set(self._resolve_tags(tag_names))

        for img in images:
            ProjectPicture.objects.create(project=instance, image=img)

        return instance
