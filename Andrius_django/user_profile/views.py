from django.contrib import messages
from django.contrib.auth import get_user_model #pasirasom papildomai
from django.contrib.auth.decorators import login_required #pasirasom papildomai
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404 #pasirasom papildomai get_object_404
from django.utils.translation import gettext_lazy as _
from . import forms

User = get_user_model()  #pasirasom paspildomai

def signup(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = forms.CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("Thank you! You can now log in with your credentials."))
            return redirect('login')
    else:
        form = forms.CreateUserForm()
    return render(request, 'user_profile/signup.html', {
        'form': form,
    })
    
@login_required   #pasirasom funkcija su dekoratorium
def user_detail(request: HttpRequest, username: str | None = None) -> HttpResponse:
    if username:
        user = get_object_or_404(User, username=username)
    else:
        user = request.user
    return render(request, 'user_profile/user_detail.html', {
        'object': user,
    })
    