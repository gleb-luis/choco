from django.urls import path
from django.contrib import admin
from django.contrib.auth.decorators import login_required 
from . import views

app_name = 'posts'

urlpatterns = [
    path('create/', login_required(views.Create.as_view()), name='create'),
    path('', views.Index.as_view(), name='index'),
    path('<int:pk>/', views.Detail,name='detail'),
    path('<int:pk>/update/', views.Update.as_view(), name='update'),
    path('<int:pk>/delete/', views.Delete.as_view(), name='delete'),
    path('search', views.Search, name='search'),
    path('like/<int:post_id>', views.like, name='like'),
    path('country/<str:country>', views.CountryDetail.as_view(), name='country_detail'),
    path('taste/<str:taste>', views.TasteDetail.as_view(), name='taste_detail'),
]