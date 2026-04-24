from rest_framework import generics, permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import NewsArticle, NewsWeeklyDigest
from .serializers import NewsArticleSerializer, NewsArticleAdminSerializer, NewsWeeklyDigestSerializer
from .filters import NewsArticleFilter


class NewsArticleListView(generics.ListAPIView):
    """Public news list — all authenticated users can read."""
    serializer_class = NewsArticleSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = NewsArticleFilter
    search_fields = ['title', 'summary', 'tags', 'source_name']
    ordering_fields = ['published_at', 'created_at']

    def get_queryset(self):
        return NewsArticle.objects.filter(is_published=True)


class NewsArticleDetailView(generics.RetrieveAPIView):
    serializer_class = NewsArticleSerializer
    queryset = NewsArticle.objects.filter(is_published=True)


class NewsArticleAdminCreateView(generics.CreateAPIView):
    """Staff-only: create a news article."""
    serializer_class = NewsArticleAdminSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class NewsArticleAdminUpdateView(generics.RetrieveUpdateDestroyAPIView):
    """Staff-only: edit/delete a news article."""
    serializer_class = NewsArticleAdminSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = NewsArticle.objects.all()


class WeeklyDigestListView(generics.ListAPIView):
    serializer_class = NewsWeeklyDigestSerializer

    def get_queryset(self):
        return NewsWeeklyDigest.objects.filter(is_published=True).prefetch_related('articles')


class WeeklyDigestDetailView(generics.RetrieveAPIView):
    serializer_class = NewsWeeklyDigestSerializer
    lookup_field = 'week_label'

    def get_queryset(self):
        return NewsWeeklyDigest.objects.filter(is_published=True).prefetch_related('articles')


class FeaturedNewsView(generics.ListAPIView):
    """Return featured articles for homepage / hero."""
    serializer_class = NewsArticleSerializer

    def get_queryset(self):
        return NewsArticle.objects.filter(is_published=True, is_featured=True)[:10]
