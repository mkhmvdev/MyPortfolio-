from django.contrib import admin
from .models import ResumeEducation , WorkExperience , Portfolio , ProfileEdit

# Register your models here.

admin.site.register(Portfolio)
admin.site.register(ResumeEducation)
admin.site.register(WorkExperience)

@admin.register(ProfileEdit)
class ProfileAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        if ProfileEdit.objects.exists():
            return False
        return True