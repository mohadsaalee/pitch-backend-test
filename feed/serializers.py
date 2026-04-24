from rest_framework import serializers
from .models import Post, PostLike, PostComment


class PostCommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.full_name', read_only=True)
    author_role = serializers.CharField(source='author.role', read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = PostComment
        fields = ['id', 'author_name', 'author_role', 'content', 'parent', 'replies', 'created_at']
        read_only_fields = ['id', 'author_name', 'author_role', 'created_at']

    def get_replies(self, obj):
        if obj.parent is None:
            return PostCommentSerializer(obj.replies.all(), many=True).data
        return []


class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.full_name', read_only=True)
    author_role = serializers.CharField(source='author.role', read_only=True)
    author_id = serializers.IntegerField(source='author.id', read_only=True)
    like_count = serializers.IntegerField(read_only=True)
    comment_count = serializers.IntegerField(read_only=True)
    liked_by_me = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'author_id', 'author_name', 'author_role',
            'post_type', 'title', 'content', 'image', 'link', 'tags',
            'is_published', 'like_count', 'comment_count', 'liked_by_me',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'author_id', 'author_name', 'author_role', 'created_at', 'updated_at']

    def get_liked_by_me(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False
