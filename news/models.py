from django.db import models
from django.conf import settings


class NewsArticle(models.Model):
    CATEGORY_CHOICES = [
        ('startup', 'Startup News'),
        ('fundraising', 'Fundraising & Investment'),
        ('ipo', 'IPO & Valuation'),
        ('venture', 'Venture Capital'),
        ('industry', 'Industry Updates'),
        ('national', 'National News'),
        ('local', 'Local Ecosystem'),
        ('policy', 'Policy & Regulation'),
        ('technology', 'Technology'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=400)
    summary = models.TextField()
    content = models.TextField(blank=True)
    source_url = models.URLField(blank=True)
    source_name = models.CharField(max_length=200, blank=True)
    image_url = models.URLField(blank=True)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='startup')
    tags = models.JSONField(default=list, blank=True)
    is_published = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    published_at = models.DateTimeField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='news_articles'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_at']

    def __str__(self):
        return self.title


class NewsWeeklyDigest(models.Model):
    """
    Groups articles into weekly digest editions.
    Updated weekly by admins or a scheduled job.
    """
    week_label = models.CharField(max_length=50, unique=True, help_text='e.g., 2025-W17')
    title = models.CharField(max_length=200)
    intro = models.TextField(blank=True)
    articles = models.ManyToManyField(NewsArticle, related_name='digests', blank=True)
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-published_at']

    def __str__(self):
        return f'Digest: {self.week_label}'
