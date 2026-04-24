from django.contrib import admin
from .models import FollowRequest, InterestMessage

@admin.register(FollowRequest)
class FollowRequestAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['sender__email', 'receiver__email']

@admin.register(InterestMessage)
class InterestMessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'tag', 'subject', 'email_sent', 'created_at']
    list_filter = ['tag', 'email_sent']
    search_fields = ['sender__email', 'receiver__email', 'subject']
