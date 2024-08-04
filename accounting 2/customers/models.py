# customers/models.py

from django.db import models
from django.conf import settings
import uuid

class Costomers(models.Model):
    name = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_customers')
    image = models.URLField(blank=True, null=True)
    tex = models.BigIntegerField(blank=True, null=True) 
    email = models.EmailField(blank=True, null=True)
    number = models.CharField(max_length=255 ,  null=True)
    is_company = models.BooleanField(default=0)
    company = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    token = models.CharField(max_length=36, unique=True, default=uuid.uuid4)

    def __str__(self):
        return self.name
