from django.urls import path
from .views import (
    FeedView, CreatePostView, PostDetailView,
    LikePostView, PostCommentsView, MyPostsView,
)

urlpatterns = [
    path('', FeedView.as_view(), name='feed'),
    path('create/', CreatePostView.as_view(), name='create-post'),
    path('my/', MyPostsView.as_view(), name='my-posts'),
    path('<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('<int:pk>/like/', LikePostView.as_view(), name='like-post'),
    path('<int:pk>/comments/', PostCommentsView.as_view(), name='post-comments'),
]
