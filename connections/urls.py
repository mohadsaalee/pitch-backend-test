from django.urls import path
from .views import (
    SendFollowRequestView, RespondFollowRequestView, UnfollowView,
    MyFollowRequestsView, MyFollowersView, MyFollowingView,
    SendInterestView, MyInterestsSentView, MyInterestsReceivedView,
)

urlpatterns = [
    # Follow
    path('follow/', SendFollowRequestView.as_view(), name='send-follow-request'),
    path('follow/<int:pk>/respond/', RespondFollowRequestView.as_view(), name='respond-follow-request'),
    path('unfollow/<int:user_id>/', UnfollowView.as_view(), name='unfollow'),
    path('requests/', MyFollowRequestsView.as_view(), name='my-follow-requests'),
    path('followers/', MyFollowersView.as_view(), name='my-followers'),
    path('following/', MyFollowingView.as_view(), name='my-following'),
    # Interest messages
    path('interest/', SendInterestView.as_view(), name='send-interest'),
    path('interest/sent/', MyInterestsSentView.as_view(), name='interests-sent'),
    path('interest/received/', MyInterestsReceivedView.as_view(), name='interests-received'),
]
