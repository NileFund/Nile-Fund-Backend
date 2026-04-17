from rest_framework import serializers
from .models import Comments

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments.author.field.related_model
        fields = ['id', 'first_name', 'last_name', 'email', 'profile_picture']
        read_only_fields = fields


class CommentDetailSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    replies = serializers.SerializerMethodField()
    
    class Meta:
        model = Comments
        fields = ['id', 'author', 'body', 'created_at', 'updated_at', 'replies']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_replies(self, obj):
        replies = obj.replies.select_related('author').order_by('created_at')
        return CommentReplySerializer(replies, many=True).data


class CommentReplySerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    
    class Meta:
        model = Comments
        fields = ['id', 'author', 'body', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ['id', 'project', 'parent', 'body', 'author', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']
        extra_kwargs = {
            'project': {'required': False, 'allow_null': True},
        }

    def validate(self, attrs):
        if self.instance is None:
            parent = attrs.get('parent')
            project = attrs.get('project')
            
            if not parent and not project:
                raise serializers.ValidationError(
                    {'non_field_errors': 'Either parent or project must be provided.'}
                )
            
            if parent:
                if project and project != parent.project:
                    raise serializers.ValidationError(
                        {'project': 'Project must match the parent comment\'s project.'}
                    )
                attrs['project'] = parent.project
        
        return attrs
