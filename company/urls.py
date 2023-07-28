from django.urls import path
from django.contrib import admin
from . import views

app_name = 'company'

urlpatterns = [
    path('terms_of_use/', views.TermsOfUseView.as_view(), name='terms_of_use'),
    path('privacy/', views.PrivacyPolicyView.as_view(), name='privacy_policy'),
    path('news/', views.NewsView.as_view(),name='news'),
    path('news/<int:pk>', views.NewsDetailView.as_view(),name='news_detail'),
    path('contact/', views.ContactView.as_view(),name='contact'),
    path('about/', views.AboutView.as_view(),name='about'),
]