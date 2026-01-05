from django.shortcuts import render
from django.views.generic import ListView
from .models import Portfolio

class View(ListView):
    template_name= "index.html"
    model = Portfolio
    context_object_name = "proekt"
    ordering = "-id"