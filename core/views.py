from django.shortcuts import render, redirect
from django.views.generic import ListView
from .models import Post, Comment
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from users.models import InUser
from django.contrib.auth.decorators import login_required
from itertools import chain
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes



class PostListView(ListView):
    model = Post
    template_name = 'discover.html'
    context_object_name = 'posts'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('-created_at')
    
    

    

@login_required()
def posts_of_following_profiles(request):
    profile = InUser.objects.get(user=request.user)
    users = [user for user in profile.following.all()]
    posts = []
    qs = None
    for user in users:
        p = InUser.objects.get(user=user)
        p_posts = p.post_set.all()
        posts.append(p_posts)
    my_posts = profile.profile_post()
    posts.append(my_posts)
    if len(posts) > 0:
        qs = sorted(chain(*posts), reverse=True, key=lambda obj: obj.created_at)
    return render(request, 'myfeed.html', {'posts': qs})

@login_required
def like_unlike_post(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Post, id=post_id)

        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user.inuser)  # Unlike
            liked = False
        else:
            post.likes.add(request.user.inuser)
            liked = True

        data = {
            
            'liked': liked,
            'total_likes': post.total_likes()
        }
        return JsonResponse(data)



