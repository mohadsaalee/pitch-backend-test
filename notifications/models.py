from django.db import models
from django.conf import settings


class Notification(models.Model):
    TYPE_CHOICES = [
        ('follow_request', 'Follow Request'),
        ('follow_accepted', 'Follow Accepted'),
        ('interest_received', 'Interest Received'),
        ('post_like', 'Post Liked'),
        ('post_comment', 'Post Commented'),
        ('new_post', 'New Post'),
    ]

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='sent_notifications'
    )
    notif_type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Notif for {self.recipient} [{self.notif_type}]'
