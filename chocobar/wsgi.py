import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chocobar.settings')

application = get_wsgi_application()

# Herokuデプロイのための追記(whitenoise3.3.1の場合は必要。5.1.0の場合は削除)
# from whitenoise.django import DjangoWhiteNoise
# application = DjangoWhiteNoise(application)
