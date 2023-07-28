from django.urls import path
from django.contrib import admin
from django.contrib.auth.decorators import login_required 
from . import views

app_name = 'column'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('create', login_required(views.Create.as_view()), name='create'),
    path('mycolumn', login_required(views.MyColumn.as_view()), name='mycolumn'),
    path('<int:pk>/', views.Detail.as_view(),name='detail'),
    path('<int:pk>/update', views.Update.as_view(), name='update'),
    path('<int:pk>/delete', views.Delete.as_view(), name='delete'),
    path('columnist', views.Columnist, name='columnist'),
]