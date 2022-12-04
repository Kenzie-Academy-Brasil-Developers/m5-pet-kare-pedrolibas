from django.db import models

class Group(models.Model):
    scientific_name = models.CharField(max_length=50, unique=True)
    created_at = models.DateField(auto_now_add=True)
    