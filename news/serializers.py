from rest_framework import serializers
from .models import NewsArticle, NewsWeeklyDigest


class NewsArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsArticle
        fields = [
            'id', 'title', 'summary', 'content', 'source_url', 'source_name',
            'image_url', 'category', 'tags', 'is_featured', 'published_at', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class NewsArticleAdminSerializer(serializers.ModelSerializer):
    """Full serializer for admin/staff to create & edit articles."""
    class Meta:
        model = NewsArticle
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class NewsWeeklyDigestSerializer(serializers.ModelSerializer):
    articles = NewsArticleSerializer(many=True, read_only=True)

    class Meta:
        model = NewsWeeklyDigest
        fields = ['id', 'week_label', 'title', 'intro', 'articles', 'published_at']
