from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserDetails(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField()
    place = models.CharField(max_length=10)

    def __str__(self):
        return self.name
    
class UserImage(models.Model):
    image = models.ImageField(upload_to='images')

class ProfileModel(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=10,default='name',null=True)

    def __str__(self):
        return self.user.username