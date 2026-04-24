from django.contrib import admin
from .models import Post, PostLike, PostComment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'post_type', 'title', 'is_published', 'created_at']
    list_filter = ['post_type', 'is_published', 'author__role']
    search_fields = ['title', 'content', 'author__email']

admin.site.register(PostLike)
admin.site.register(PostComment)
