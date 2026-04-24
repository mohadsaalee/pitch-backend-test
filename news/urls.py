from django.urls import path
from .views import (
    NewsArticleListView, NewsArticleDetailView,
    NewsArticleAdminCreateView, NewsArticleAdminUpdateView,
    WeeklyDigestListView, WeeklyDigestDetailView, FeaturedNewsView,
)

urlpatterns = [
    path('', NewsArticleListView.as_view(), name='news-list'),
    path('featured/', FeaturedNewsView.as_view(), name='news-featured'),
    path('<int:pk>/', NewsArticleDetailView.as_view(), name='news-detail'),
    # Admin
    path('admin/create/', NewsArticleAdminCreateView.as_view(), name='news-admin-create'),
    path('admin/<int:pk>/', NewsArticleAdminUpdateView.as_view(), name='news-admin-update'),
    # Digests
    path('digest/', WeeklyDigestListView.as_view(), name='digest-list'),
    path('digest/<str:week_label>/', WeeklyDigestDetailView.as_view(), name='digest-detail'),
]
