from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.utils import timezone, dateformat
from django.http import HttpResponse
from django.views import generic
from django.db.models import F, Q
from django.contrib import messages #　検索結果のメッセージのため追加

from .forms import SignUpForm, activate_user


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('activate_email_sent')
    template_name = 'registration/signup.html'
    
    
class ActivateView(TemplateView):
    template_name = "registration/activate.html"
    
    def get(self, request, uidb64, token, *args, **kwargs):
        result = activate_user(uidb64, token)
        return super().get(request, result=result, **kwargs)

