from django.contrib import admin
from django.urls import include, path
from core.views import PostListView, posts_of_following_profiles, like_unlike_post
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('discover', PostListView.as_view(), name="discover"),
    path('', posts_of_following_profiles, name="feed"),
    path('like/', like_unlike_post, name='like_unlike_post'),
    
]