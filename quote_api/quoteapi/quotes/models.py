from django.db import models

# Create your models here.
class Quote(models.Model):
    text = models.CharField(max_length=1000)
    author = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)