from .models import Country, Taste

def common(request):
    """テンプレートに毎回渡すデータ"""
    context = {
        'country_list': Country.objects.all(),
        'taste_list': Taste.objects.all(),
    }

    return context
