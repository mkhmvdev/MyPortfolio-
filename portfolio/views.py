from django.views.generic import ListView
from .models import Portfolio, ResumeEducation , WorkExperience

class View(ListView):
    model = Portfolio
    template_name = "index.html"
    context_object_name = "projects"
    ordering = "-id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["works"] = WorkExperience.objects.all().order_by("-id")
        context["educations"] = ResumeEducation.objects.all().order_by("-id")
        return context
