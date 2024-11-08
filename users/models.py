from django.db import models
from django.contrib.auth.models import User



class InUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='inuser')
    following = models.ManyToManyField(User, related_name="following", blank=True)
    created = models.DateTimeField(auto_now_add=True)
    about = models.TextField(max_length=50, null=True, blank=True)
    image = models.ImageField(default='profile_pics/blank-profile-picture-973460_1280.png', upload_to='profile_pics')

    def profile_post(self):
        return self.post_set.all()
    
    def total_comments(self):
        from core.models import Comment  # Local import
        return Comment.objects.filter(post__author=self).count()

    def __str__(self):
        return f"{self.user.username.title()}'s Profile"
    
    @property
    def followers(self):
        return InUser.objects.filter(following=self.user)
    
    class Meta:
        ordering = ('-created',)
    

        