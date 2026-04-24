from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from .models import Post, PostLike, PostComment
from .serializers import PostSerializer, PostCommentSerializer
from connections.models import FollowRequest
from notifications.utils import create_notification

User = get_user_model()


class FeedView(generics.ListAPIView):
    """
    Main feed: posts from users the current user follows
    + all public-role users' posts + own posts.
    Supports filtering by post_type and searching.
    """
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['post_type', 'author__role']
    search_fields = ['title', 'content', 'tags']
    ordering_fields = ['created_at', 'like_count']

    def get_queryset(self):
        user = self.request.user
        # IDs of followed users (accepted)
        following_ids = FollowRequest.objects.filter(
            sender=user, status='accepted'
        ).values_list('receiver_id', flat=True)

        # Public-role user IDs
        public_user_ids = User.objects.filter(
            role__in=['investor', 'consultant', 'ecosystem_partner']
        ).values_list('id', flat=True)

        visible_ids = set(following_ids) | set(public_user_ids) | {user.id}
        return Post.objects.filter(
            author_id__in=visible_ids, is_published=True
        ).select_related('author').prefetch_related('likes', 'comments')


class CreatePostView(generics.CreateAPIView):
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        post = serializer.save(author=self.request.user)
        # Notify followers
        followers = FollowRequest.objects.filter(
            receiver=self.request.user, status='accepted'
        ).select_related('sender')
        for fr in followers:
            create_notification(
                recipient=fr.sender,
                sender=self.request.user,
                notif_type='new_post',
                message=f'{self.request.user.full_name} published a new post.',
            )


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get_permissions(self):
        if self.request.method in ('PUT', 'PATCH', 'DELETE'):
            from rest_framework.permissions import IsAuthenticated
            return [IsAuthenticated()]
        return [permissions.IsAuthenticated()]

    def update(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            return Response({'detail': 'Permission denied.'}, status=403)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            return Response({'detail': 'Permission denied.'}, status=403)
        return super().destroy(request, *args, **kwargs)


class LikePostView(APIView):
    """Toggle like on a post."""

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk, is_published=True)
        like, created = PostLike.objects.get_or_create(post=post, user=request.user)
        if not created:
            like.delete()
            return Response({'liked': False, 'like_count': post.like_count})
        create_notification(
            recipient=post.author,
            sender=request.user,
            notif_type='post_like',
            message=f'{request.user.full_name} liked your post.',
        )
        return Response({'liked': True, 'like_count': post.like_count})


class PostCommentsView(generics.ListCreateAPIView):
    serializer_class = PostCommentSerializer

    def get_queryset(self):
        return PostComment.objects.filter(
            post_id=self.kwargs['pk'], parent=None
        ).select_related('author').prefetch_related('replies__author')

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        comment = serializer.save(author=self.request.user, post=post)
        create_notification(
            recipient=post.author,
            sender=self.request.user,
            notif_type='post_comment',
            message=f'{self.request.user.full_name} commented on your post.',
        )


class MyPostsView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).select_related('author')
