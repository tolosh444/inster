from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (UserDetailAPI,RegisterUserView,
                    create_post_view, UserProfileUpdateAPI,
                    FollowCountAPI, FollowUnfollowInUserAPI,
                    add_comment, PostDeleteView)
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("get-details",UserDetailAPI.as_view()),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('create-post/', create_post_view, name='create-post'),
    path('api/profile/update/', UserProfileUpdateAPI.as_view(), name='profile-update-api'),
    path('profile/follow-count/', FollowCountAPI.as_view(), name='follow-count'),
    path('follow-unfollow/', FollowUnfollowInUserAPI.as_view(), name='follow_unfollow'),
    path('api/posts/<int:post_id>/comment/', add_comment, name='add_comment'),
    path('posts/<int:pk>/', PostDeleteView.as_view(), name='post-delete'),
    ]