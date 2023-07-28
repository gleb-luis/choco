from django.contrib import admin
from django.urls import path, include  # 修正  urlsのファイルを読み込むincludeを追加
from django.views.static import serve  # 後に使うviewsのファイルを追加 
from django.conf import settings # プロジェクトの設定を読み込むプログラムを呼び出す部分を追加

from django.contrib.auth import views as auth_views #各SNSからのログインで追加
from accounts import views #各SNSからのログインで追加

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),#usernameログイン
    path('accounts/', include('accounts.urls')),
    path('posts', include('posts.urls')),
    path('column/', include('column.urls')),
    path('', include('shop.urls')),
    path('company/', include('company.urls')),
    path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
    path('summernote/', include('django_summernote.urls')),
    path('', include('social_django.urls', namespace="social")),#各SNSからのログイン
]

# When debug option is enabled(DEBUG=True), DO NOT forget to add urlpatterns as shown below:
from django.conf.urls.static import static
 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)