from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from . import models


def index(request: HttpRequest) -> HttpResponse:
    context = {
        'projects_count': models.Project.objects.count(),
        'task_count': models.Task.objects.count(),
        'user_count': 
    }
    

# Create your views here.
