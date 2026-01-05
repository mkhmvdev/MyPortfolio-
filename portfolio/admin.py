from django.contrib import admin
from .models import Portfolio
from .models import ResumeEducation
from .models import WorkExperience

# Register your models here.

admin.site.register(Portfolio)
admin.site.register(ResumeEducation)
admin.site.register(WorkExperience)

