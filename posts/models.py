import datetime
from django.urls import reverse
from django.db import models
from accounting.models import User


class Posts(models.Model):
    caption = models.CharField(max_length=255)
    img = models.FileField(null=True, blank=True)
    # created = models.DateTimeField(auto_now_add=True)
    # updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True)

    def get_absolute_url(self):
        return reverse('posts:like', args=[self.id, ])

    @property
    def user_profile(self):
        return self.owner.profile if hasattr(self.owner, 'profile') else None


class Likes(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users')
