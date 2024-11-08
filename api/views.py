from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import UserSerializer,RegisterSerializer, PostSerializer
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import login
from core.models import Post, Comment
from django.contrib.auth.decorators import login_required
from users.models import InUser
from rest_framework.permissions import IsAuthenticated
from .serializers import UserUpdateSerializer, ProfileUpdateSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404


# Class based view to Get User Details using Token Authentication
class UserDetailAPI(APIView):
  authentication_classes = (TokenAuthentication,)
  permission_classes = (AllowAny,)
  def get(self,request,*args,**kwargs):
    user = User.objects.get(id=request.user.id)
    serializer = UserSerializer(user)
    return Response(serializer.data)

#Class based view to register user
class RegisterUserAPIView(generics.CreateAPIView):
  permission_classes = (AllowAny,)
  serializer_class = RegisterSerializer
  
class RegisterUserView(View):
    def get(self, request, *args, **kwargs):
        form = RegisterSerializer()
        return render(request, 'register.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = RegisterSerializer(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('feed')  
        return render(request, 'register.html', {'form': form})
    
    
@login_required()   
def create_post_view(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        post_photo = request.FILES.get('post_photo')
        in_user = InUser.objects.get(user=request.user)
        # Create a new post with the logged-in user as the author
        post = Post.objects.create(
            content=content,
            post_photo=post_photo,
            author=in_user
        )
        
        return redirect("/")  # Redirect to some page after successful post creation

    return render(request, 'post_create.html')
  
  
class UserProfileUpdateAPI(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user

        
        try:
            profile = request.user.inuser 
        except InUser.DoesNotExist:
            return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

        u_serializer = UserUpdateSerializer(user, data=request.data)
        p_serializer = ProfileUpdateSerializer(profile, data=request.data)

        if u_serializer.is_valid() and p_serializer.is_valid():
            u_serializer.save()
            p_serializer.save()
            return Response({"message": "Profile updated successfully"}, status=status.HTTP_200_OK)

        return Response({
            "user_errors": u_serializer.errors,
            "profile_errors": p_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)



        
class FollowCountAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        my_profile = InUser.objects.get(user=request.user)
        follow_count = my_profile.following.all().count()
        return Response({'follow_count': follow_count}, status=status.HTTP_200_OK)


class FollowUnfollowInUserAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        my_profile = InUser.objects.get(user=request.user)
        profile_pk = request.data.get('profile_pk')

        try:
            obj = InUser.objects.get(pk=profile_pk)
        except InUser.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Toggle follow/unfollow
        if obj.user in my_profile.following.all():
            my_profile.following.remove(obj.user)
            action = 'unfollowed'
        else:
            my_profile.following.add(obj.user)
            action = 'followed'

        return Response({
            'message': f'You have {action} {obj.user.username}.',
            'following_count': my_profile.following.count(),
        }, status=status.HTTP_200_OK)
        
        
@api_view(['POST'])
@permission_classes([AllowAny])
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    content = request.data.get('content')
    
    
    try:
        author = InUser.objects.get(user=request.user)
    except InUser.DoesNotExist:
        return Response({'error': 'User  does not have an associated InUser  instance.'}, status=status.HTTP_400_BAD_REQUEST)


    if content:
        comment = Comment.objects.create(post=post, author=author, content=content)
        return Response({'message': 'Comment added successfully'}, status=status.HTTP_201_CREATED)
    return Response({'error': 'Content cannot be empty'}, status=status.HTTP_400_BAD_REQUEST)

class PostDeleteView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        instance.delete()

    def delete(self, request, *args, **kwargs):
        self.perform_destroy(self.get_object())
        return Response({'message': 'Post deleted successfully'}, status=status.HTTP_200_OK)