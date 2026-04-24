from django.db import models
from django.conf import settings


class Post(models.Model):
    POST_TYPE_CHOICES = [
        ('update', 'General Update'),
        ('news', 'Company News'),
        ('program', 'Upcoming Program'),  # ecosystem partners
        ('fundraise', 'Fundraising Update'),
        ('milestone', 'Milestone'),
        ('hiring', 'Hiring'),
        ('other', 'Other'),
    ]

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts'
    )
    post_type = models.CharField(max_length=20, choices=POST_TYPE_CHOICES, default='update')
    title = models.CharField(max_length=300, blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to='feed/', blank=True, null=True)
    link = models.URLField(blank=True)
    tags = models.JSONField(default=list, blank=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.author.full_name} — {self.post_type} ({self.created_at.date()})'

    @property
    def like_count(self):
        return self.likes.count()

    @property
    def comment_count(self):
        return self.comments.count()


class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='liked_posts')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')


class PostComment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Comment by {self.author.full_name} on Post {self.post_id}'
