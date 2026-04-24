from django.contrib import admin
from .models import NewsArticle, NewsWeeklyDigest

@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'is_featured', 'is_published', 'published_at']
    list_filter = ['category', 'is_featured', 'is_published']
    search_fields = ['title', 'summary']
    list_editable = ['is_featured', 'is_published']
    date_hierarchy = 'published_at'

@admin.register(NewsWeeklyDigest)
class WeeklyDigestAdmin(admin.ModelAdmin):
    list_display = ['week_label', 'title', 'is_published', 'published_at']
    filter_horizontal = ['articles']
