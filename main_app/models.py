from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

class Art(models.Model):
    name = models.CharField(max_length=100)
    mediums = models.CharField(max_length=150)
    description = models.TextField(max_length=250)
    date = models.DateField('Date Completed')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'art_id': self.id})

class Profile(models.Model):
    artist_name = models.CharField(max_length=100)
    statement = models.TextField(max_length=350)
    about = models.TextField(max_length=550)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.artist_name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'profile_id': self.id})
class PhotoArt(models.Model):
    url = models.CharField(max_length=200)
    art = models.ForeignKey(Art, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for art_id: {self.art_id} @{self.url}"

class PhotoProfile(models.Model):
    url = models.CharField(max_length=200)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for profile_id: {self.profile_id} @{self.url}"
