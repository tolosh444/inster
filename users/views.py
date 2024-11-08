from django.shortcuts import  redirect, render
from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import InUser
from core.models import Post
from django.db.models import Count
from django.http import HttpResponseRedirect


def logout_view(request):
    if request.method in ['GET', 'POST']:
        logout(request)
        return redirect('feed')


def profile_view(request):
    inuser = InUser.objects.get(user=request.user)  # Get the user's profile
    post = inuser.post_set.all().order_by('-created_at')
    posts_count = inuser.post_set.count
    followers_count = inuser.followers.count() 
    total_likes = Post.objects.filter(author=inuser).aggregate(total_likes=Count('likes'))['total_likes']
    total_comments = inuser.total_comments()
    
    
    context = {
        'profile': inuser,
        'p_posts': post,
        'posts_count': posts_count,
        'followers_count': followers_count,
        'total_likes': total_likes,
        'total_comments': total_comments,
        
    }
    return render(request, 'profile.html', context)





def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    inuser = get_object_or_404(InUser, user=user)
    posts = inuser.profile_post()  
    followers_count = inuser.followers.count() 
    posts_count = inuser.post_set.count
    is_following = inuser.user in request.user.inuser.following.all() 
    total_likes = Post.objects.filter(author=inuser).aggregate(total_likes=Count('likes'))['total_likes']
    total_comments = inuser.total_comments()
    context = {
        'user_profile': inuser,
        'posts': posts,
        'followers_count': followers_count,
        'posts_count': posts_count,
        'is_following': is_following,
        'total_likes': total_likes,
        'total_comments': total_comments,
        
        
    }
    return render(request, 'users_details.html', context)




@login_required()
def follow_unfollow_profile(request):
    if request.method == 'POST':
        my_profile = InUser.objects.get(user=request.user)
        pk = request.POST.get('profile_pk')
        obj = InUser.objects.get(pk=pk)

        if obj.user in my_profile.following.all():
            my_profile.following.remove(obj.user)
        else:
            my_profile.following.add(obj.user)
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('user-profile')



@login_required
def update_profile_page(request):
    return render(request, 'update_profile.html')


def user_search(request):
    
    searched = request.GET['searched']
    users = User.objects.all()
    if not searched:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    searched_users = User.objects.filter(username__icontains=searched).distinct()
    
    context = {
        "searched": searched,
        "users": searched_users,
    }
    
    return render(request, "search.html", context)
