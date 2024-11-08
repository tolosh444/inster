from django.db import models
from django.utils import timezone
from django.urls import reverse
from users.models import InUser
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

class Post(models.Model):
    content = models.TextField(verbose_name='Content')
    created_at = models.DateTimeField(default=timezone.now)
    post_photo = models.ImageField(upload_to='post_photoes' ,null=True, blank=True)
    author = models.ForeignKey(InUser, on_delete=models.CASCADE)
    likes = models.ManyToManyField(InUser, related_name='liked_posts', blank=True)


    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return f"Author - {self.author.user.username.title()} , post ID - {self.id}"
    
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(InUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Author - {self.author.user.username.title()}, post ID - {self.post.id}'


    
    