import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ALLOWED_HOSTS = ['choco.fan', 'www.choco.fan']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts.apps.AccountsConfig',   # アカウント管理のアプリを追加
    'posts',
    'django_cleanup', # 投稿削除時に画像も削除する
    'column',
    'shop',
    'company',# アドミン的な機能を行うアプリ
    'django_summernote',#WYSIWYGエディタ
    'widget_tweaks',#フォームのデザインをやりやすくする
    'social_django',#各SNSアカウントからのログイン "pip install social-auth-app-django"後に追加。追加後に必ず"python manage.py migrate"
    'storages',#S3ログインで追加
    'django.contrib.sites',
    'sitesetting',#サイト共通設定のアプリ名
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',# SNSログインのために追加
    'django.contrib.sites.middleware.CurrentSiteMiddleware',#Siteの内容をいつも表示するためのもの。ContextProcessorは使わなくてよい。
]

ROOT_URLCONF = 'chocobar.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'DIRS': [],
        'DIRS': [os.path.join(BASE_DIR, 'templates')],# テンプレートが入っているディレクトリを指定
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'posts.context_processors.common',#追加
                'shop.context_processors.all_pref',#追加
                'social_django.context_processors.backends', # FBloginで追加 username以外のデータもとる為
                'social_django.context_processors.login_redirect', # FBloginで追加 username以外のデータもとる為
            ],
        },
    },
]

WSGI_APPLICATION = 'chocobar.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SUMMERNOTE_THEME = 'bs4'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)

# 参照　http://whitenoise.evans.io/en/stable/django.html#django-middleware
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# 追加
AUTH_USER_MODEL = 'accounts.User' # アカウント管理で使うモデル(後述)を指定する行を追加

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = 'shop:index'


# SNSログインのために追加
AUTHENTICATION_BACKENDS = (
    'social_core.backends.open_id.OpenIdAuth',
    'social_core.backends.google.GoogleOpenId',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.linkedin.LinkedinOAuth2',
    'social_core.backends.yahoo.YahooOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_URL_NAMESPACE = 'social'

# Facebook login
# SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {"fields": "id,name,email",}
SOCIAL_AUTH_FIELD_SELECTORS = ["name",]

# SOCIAL_AUTH_FACEBOOK_SCOPE = ['email', 'user_link']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'fields': 'id, name, email, picture.type(large), link'
}
SOCIAL_AUTH_FACEBOOK_EXTRA_DATA = [
    ('name', 'name'),
    ('email', 'email'),
    ('picture', 'icon'),
    ('link', 'fb'),
]

# Instagramログイン
SOCIAL_AUTH_INSTAGRAM_EXTRA_DATA = [('user', 'user'),]
SOCIAL_AUTH_INSTAGRAM_AUTH_EXTRA_ARGUMENTS = {'scope': 'likes comments relationships'}

# ログイン後のリダイレクト先
SOCIAL_AUTH_LOGIN_REDIRECT_URL = 'shop:index'

# Herokuへのデプロイのために追記
import dj_database_url
DATABASES['default'] = dj_database_url.config()

# SSLリダイレクト
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

DEBUG = False

# AWS S3のための設定
# AWS S3 共通の設定

AWS_STORAGE_BUCKET_NAME = 'choco-fan'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',  # 1日はそのキャッシュを使う
}

# AWS S3 メディアファイルの設定。「chocobar」はプロジェクト名
AWS_LOCATION = 'media'
# DEFAULT_FILE_STORAGE = 'chocobar.backends.MediaStorage' settings.pyと同じ階層にbackends.pyを記述する場合
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
file_overwrite = False  # 同名ファイルは上書きせずに似た名前のファイルに

# メール送信の設定　TODO本番環境向けにherokuにセットする
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True



try:
    from .local_settings import *
except ImportError:
    SECRET_KEY = os.environ['SECRET_KEY']
    EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
    EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
    SOCIAL_AUTH_INSTAGRAM_KEY = os.environ['SOCIAL_AUTH_INSTAGRAM_KEY']
    SOCIAL_AUTH_INSTAGRAM_SECRET = os.environ['SOCIAL_AUTH_INSTAGRAM_SECRET']
    SOCIAL_AUTH_TWITTER_KEY = os.environ['SOCIAL_AUTH_TWITTER_KEY']
    SOCIAL_AUTH_TWITTER_SECRET = os.environ['SOCIAL_AUTH_TWITTER_SECRET']
    SOCIAL_AUTH_FACEBOOK_KEY = os.environ['SOCIAL_AUTH_FACEBOOK_KEY']
    SOCIAL_AUTH_FACEBOOK_SECRET = os.environ['SOCIAL_AUTH_FACEBOOK_SECRET']
    SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ['SOCIAL_AUTH_GOOGLE_OAUTH2_KEY']
    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ['SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET']
    pass

