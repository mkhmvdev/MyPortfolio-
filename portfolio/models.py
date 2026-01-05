from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Portfolio(models.Model):
    name = models.CharField(max_length=30)
    image = models.ImageField(
        upload_to='portfolio/',
        blank=True,
        null=True
    )
    
    def __str__(self):
        return self.name
    
    
    class Meta:
        verbose_name = "proekt" 
        verbose_name_plural = "portfolio"

