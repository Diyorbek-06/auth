from django.db import models

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=300)
    short_desc = models.CharField(max_length=300)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
