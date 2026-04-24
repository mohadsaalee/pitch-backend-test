from django.db import models
from django.conf import settings


class FollowRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_requests'
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_requests'
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    message = models.TextField(blank=True, help_text='Optional introductory message')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('sender', 'receiver')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.sender} -> {self.receiver} [{self.status}]'


class InterestMessage(models.Model):
    """
    Interest/outreach message sent via email (MVP communication layer).
    Tags categorize the type of interest.
    """
    TAG_CHOICES = [
        ('investment', 'Investment Interest'),
        ('collaboration', 'Collaboration'),
        ('mentorship', 'Mentorship'),
        ('partnership', 'Partnership'),
        ('hiring', 'Hiring'),
        ('advisory', 'Advisory'),
        ('general', 'General Inquiry'),
    ]

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_interests'
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_interests'
    )
    tag = models.CharField(max_length=20, choices=TAG_CHOICES, default='general')
    subject = models.CharField(max_length=200)
    message = models.TextField()
    email_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Interest from {self.sender} to {self.receiver} [{self.tag}]'
