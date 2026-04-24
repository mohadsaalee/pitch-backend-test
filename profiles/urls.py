from django.urls import path
from .views import MyProfileView, UserProfileView, PublicProfilesListView

urlpatterns = [
    path('me/', MyProfileView.as_view(), name='my-profile'),
    path('public/', PublicProfilesListView.as_view(), name='public-profiles'),
    path('<int:user_id>/', UserProfileView.as_view(), name='user-profile'),
]
