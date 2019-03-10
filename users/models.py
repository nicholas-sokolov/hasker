from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, models.CASCADE)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    register_date = models.DateField(auto_now=True)
    website = models.URLField(blank=True)

    def __unicode__(self):
        return f'Profile of {self.user.username}'
