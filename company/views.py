from django.shortcuts import render, redirect
from django.views import generic
from django.views.generic import TemplateView, ListView, DetailView
from django.urls import reverse_lazy
from django.views import  View 
from .models import CompanyInfo, TermsOfUse, PrivacyPolicy, News
from django.contrib import messages


class TermsOfUseView(TemplateView):
    template_name = 'company/terms_of_use.html'

    def get_context_data(self, **kwargs):
        context = TermsOfUse.objects.all().order_by('-created_at')[:1]
        params = {
            'context': context,
        }
        return params


class PrivacyPolicyView(TemplateView):
    template_name = 'company/privacy.html'

    def get_context_data(self, **kwargs):
        context = PrivacyPolicy.objects.all().order_by('-created_at')[:1]
        params = {
            'context': context,
        }
        return params


class NewsView(ListView):
    template_name = 'company/news.html'
    model = News
    paginate_by = 20


class NewsDetailView(DetailView):
    model = News


class ContactView(TemplateView):
    template_name = 'company/contact.html'


class AboutView(TemplateView):
    template_name = 'company/about.html'