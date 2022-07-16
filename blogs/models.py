from django.db import models

# Create your models here.

class ProtectedBlog(models.Model):
    time_created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    strapline = models.TextField(max_length=500, blank=True)
    is_encrypted = models.BooleanField()
    private_key = models.TextField(max_length=200, blank=True)
    blog_content = models.TextField()
    author = models.CharField(max_length=100, blank=True)
    attributed_name = models.CharField(max_length=50, blank=True)