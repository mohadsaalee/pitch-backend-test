import django_filters
from .models import NewsArticle


class NewsArticleFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(lookup_expr='exact')
    is_featured = django_filters.BooleanFilter()
    published_after = django_filters.DateTimeFilter(field_name='published_at', lookup_expr='gte')
    published_before = django_filters.DateTimeFilter(field_name='published_at', lookup_expr='lte')

    class Meta:
        model = NewsArticle
        fields = ['category', 'is_featured']
