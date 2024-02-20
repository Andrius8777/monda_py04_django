from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import gettext_lazy as _
from . import models
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin #class base views sablonai
from django.views import generic
from django.urls import reverse


class ProjectListView(generic.ListView):
    model = models.Project                             #nusirodom modeli
    template_name = 'tasks/project_list.html'          #nusirodom tempalte

class ProjectDetailView(generic.DetailView):
    model = models.Project
    template_name = 'tasks/project_detail.html'


class ProjectCreateView(LoginRequiredMixin, generic.CreateView):    #LoginRequiredMixin turi eiti pirmas
    model = models.Project                                          #nusirodom modeli
    template_name = 'tasks/project_create.html'                     #nusirodom templagte name
    fields = ('name', )                                             #nusirodo laukus kokius useris pildys
    
    def get_success_url(self) -> str:                               #modifikuojam 2 metodus
        messages.success(self.request, 
            _('project created succesfully').capitalize())          #ismesim zinute 
        return reverse('project_list')
    
    def form_valid(self, form):                                     #jeigu forma bus teisingai uzpildyta 
        form.instance.owner = self.request.user                     #ja pasieksim tik self.request.user              return super().form_valid(form)


def index(request: HttpRequest) -> HttpResponse:
    context = {
        'projects_count': models.Project.objects.count(),
        'tasks_count': models.Task.objects.count(),
        'users_count': models.get_user_model().objects.count(),
    }
    return render(request, 'tasks/index.html', context)

def task_list(request: HttpRequest) -> HttpResponse:
    return render(request, 'tasks/task_list.html', {
        'task_list': models.Task.objects.all(),
    })

def task_detail(request: HttpRequest, pk: int) -> HttpResponse:
    return render(request, 'tasks/task_detail.html', {
        'task': get_object_or_404(models.Task, pk=pk),
    })

def task_done(request: HttpRequest, pk: int) -> HttpResponse:
    task = get_object_or_404(models.Task, pk=pk)
    task.is_done = not task.is_done
    task.save()
    messages.success(request, "{} {} {} {}".format(
        _('task').capitalize(),
        task.name,
        _('marked as'),
        _('done') if task.is_done else _('undone'),
    ))
    if request.GET.get('next'):
        return redirect(request.GET.get('next'))
    return redirect(task_list)
