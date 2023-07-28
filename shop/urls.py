from django.urls import path
from django.contrib import admin
from django.contrib.auth.decorators import login_required 
from . import views

app_name = 'shop'

urlpatterns = [
    path('shop/create', login_required(views.Create.as_view()), name='create'),
    path('', views.Index.as_view(), name='index'),
    path('shop/<str:name>', views.ShopDetail.as_view(),name='detail'),#フォルダをshopにしないとsearchがおかしくなる
    path('shop/<str:name>/update', views.Update.as_view(), name='shop_update'),
    path('shop/<str:name>/delete', views.Delete.as_view(), name='shop_delete'),
    path('shop/like/<str:name>', views.Like_shop, name='like_shop'),
    path('shop/delete/<str:name>', views.Like_shop_delete, name="like_shop_delete"),
    path('review/<int:pk>/update', views.ReviewUpdate.as_view(), name='review_update'),
    path('review/<int:pk>/delete', views.ReviewDelete.as_view(), name='review_delete'),    
    path('search', views.Search, name='search'),
    path('shop/owner_list', views.OwnerList, name='owner_list'),
    path('upload', views.shop_upload, name='upload'),
    path('export/', views.shop_export, name='export'),
    path('shoplist', views.ShopList.as_view(), name='shop_list'),
    path('shoplist/<str:name>', views.PrefDetail.as_view(), name='pref_shop_list'),
    path('tag/<str:name>', views.TagDetail.as_view(), name='tag_shop_list'),
    path('user/about', views.About_user.as_view(), name='about_user'),
    path('owner/about', views.About_owner.as_view(), name='about_owner'),
]