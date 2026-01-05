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
    context_object_name = "potfolio"
    
    def __str__(self):
        return self.name
    
    
    class Meta:
        verbose_name = "proekt" 
        verbose_name_plural = "portfolio"

class ResumeEducation(models.Model):
    study_name = models.CharField(max_length=30 )
    study_year = models.IntegerField(("O‘qish yili"))
    study_about = models.TextField()
    context_object_name = "educations"
    
    def __str__(self):
        return self.study_name
    
    class Meta:
        verbose_name = "O'qish" 
        verbose_name_plural = "Kurs"
        
        
class WorkExperience(models.Model):
    company_name = models.CharField(max_length=30 )
    company_year = models.IntegerField(("ish yili"))
    company_about = models.TextField()
    context_object_name = "work"

    def __str__(self):
        return self.company_name
    
    class Meta:
        verbose_name = "Tajriba" 
        verbose_name_plural = "Ish"
    