from .models import Pref, Shop, Tag

def all_pref(request):
    """テンプレートに毎回渡すデータ"""
    recommended_shop_list = Shop.objects.all()[:6]

    context = {
        'pref_list': Pref.objects.all(),
        'tag_list': Tag.objects.all(),
        'recommended_shop_list': recommended_shop_list,
    }

    return context
