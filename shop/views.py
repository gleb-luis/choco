from django.shortcuts import render, resolve_url, redirect
from django.views import generic
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views import  View 
from .forms import ShopForm, SearchForm, ReviewForm
from .models import Shop, Pref, ReviewShop, LikeShop, Tag
from column.models import Column
from accounts.models import User
from company.models import PageSetting, News
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.db.models import Q, Avg

# 検索のために追加 参考 https://django.kurodigi.com/search_page/
from functools import reduce
from operator import and_

# CSVインポート エクスポート
import csv
from io import TextIOWrapper, StringIO
from django.http import HttpResponse


# update deleteに使う
class OnlyYourShopMixin(UserPassesTestMixin):
    raise_exception = True
    # 自分がオーナーのShopのみ
    def test_func(self):
        shop = Shop.objects.get(name = self.kwargs['name'])
        return shop.owner == self.request.user


class OnlyYourReviewMixin(UserPassesTestMixin):
    raise_exception = True
    # 自分が書いたのreviewのみ
    def test_func(self):
        review = ReviewShop.objects.get(id = self.kwargs['pk'])
        return review.user == self.request.user


class Create(CreateView):
    template_name = 'shop/create.html'
    form_class = ShopForm
    success_url = reverse_lazy('shop:index')

    # 入力に問題がない場合現在ログインしているアカウントをownerとして登録するための処理
    def form_valid(self, form):
        form.instance.owner_id = self.request.user.id
        form.off_flag = False
        return super(Create, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, '新しい店舗を登録しました！')
        return resolve_url('shop:index')


class Index(TemplateView):
    template_name = 'shop/index.html'

    def get_context_data(self, *args, **kwargs):
        searchform = SearchForm()
        shop_list = Shop.objects.filter(off_flag=False).order_by('-views').reverse()[:12]
        column_list = Column.objects.filter(is_draft=False, author__is_owner=False).order_by('-created_at')[:6]
        owners_column_list = Column.objects.filter(is_draft=False, author__is_owner=True).order_by('-created_at')[:6]
        news_list = News.objects.all().order_by('-public_date')[:5]

        params = {
            'searchform': searchform,
            'shop_list': shop_list,
            'column_list': column_list,
            'owners_column_list': owners_column_list,
            'news_list': news_list,
            }
        return params


# 店舗の方向け
class About_owner(TemplateView):
    template_name = 'shop/about_owner.html'


# 一般の方向け
class About_user(TemplateView):
    template_name = 'shop/about_user.html'
    

def Search(request):
    if request.method == 'POST':
        searchform = SearchForm(request.POST)

        if searchform.is_valid():
            freeword = searchform.cleaned_data['freeword']
            pref = request.POST['pref']
            tag = []

            if freeword :
                search_list = Shop.objects.filter(Q(off_flag__contains = "False")|Q(content__icontains = freeword)|Q(name__icontains = freeword)|Q(short_content__icontains = freeword)|Q(pref__name = pref))            
            else:
                search_list = Shop.objects.filter(Q(off_flag__contains = "False")|Q(pref__name = pref)) 

        params = {
            'shop_list': search_list,
            }

        return render (request, 'shop/search.html', params)


class Update(OnlyYourShopMixin, UpdateView):
    model = Shop
    slug_field = 'name'  # モデルのフィールドの名前
    slug_url_kwarg = 'name'  # urls.pyでのキーワードの名前
    form_class = ShopForm
    template_name = 'shop/update.html'

    def get_success_url(self):
        messages.success(self.request, 'ショップ情報を更新しました！')
        return resolve_url('shop:index')


class Delete(OnlyYourShopMixin, DeleteView):
    model = Shop
    slug_field = 'name'  # モデルのフィールドの名前
    slug_url_kwarg = 'name'  # urls.pyでのキーワードの名前
    success_url = reverse_lazy('shop:index')
    template_name = 'shop/delete.html'

    def delete(self, request, *args, **kwargs):
        result = super().delete(request, *args, **kwargs)
        messages.success(
            self.request, '「{}」を削除しました'.format(self.object))
        return result


class ShopList(ListView):
    model = Shop
    template_name = 'shop/shoplist.html'
    paginate_by = 12
    
    def get_queryset(self):
        shop_list = Shop.objects.filter(off_flag=False).order_by('pref')
        return shop_list    
           

class ShopDetail(DetailView):
    model = Shop
    slug_field = 'name'  # モデルのフィールドの名前
    slug_url_kwarg = 'name'  # urls.pyでのキーワードの名前

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            like_shop = LikeShop.objects.filter(liked_by = self.request.user, shop = kwargs['object'])
        else:
            like_shop = False
        detail_data = Shop.objects.get(name = self.kwargs['name'])#getにすることでオブジェクトを取得。filterだとQueryを取得になってしまう。
        detail_data.views += 1 #アクセス数をいったんカウントアップして保存
        detail_data.save()
        users_shop_list = Shop.objects.filter(off_flag=False).filter(owner = detail_data.owner)#サイドバーに表示
        pref_shop_list = Shop.objects.filter(off_flag=False).filter(pref = detail_data.pref).order_by('views')[:5]#サイドバーに表示
        owners_column = Column.objects.filter(author = detail_data.owner).order_by('-created_at')
        average_score = ReviewShop.objects.filter(shop=detail_data.id).aggregate(Avg('score'))
        average = average_score['score__avg']
        if average:
            average_rate = average / 5 * 100
        else:
            average_rate = 0

        review_form = ReviewForm()
        review_list = ReviewShop.objects.filter(shop=detail_data.id)
        detail_data.save()

        params = {
            'like_shop': like_shop,
            'object': detail_data,
            'review_form': review_form,
            'review_list': review_list,
            'average_rate': average_rate,
            'users_shop_list': users_shop_list,
            'pref_shop_list': pref_shop_list,
            'owners_column': owners_column,
            }

        return params
        
    def post(self, request, *args, **kwargs):
        detail_data = Shop.objects.get(name = self.kwargs['name'])
        form = ReviewForm(data=request.POST)
        # comment = request.POST['comment']

        if form.is_valid():
            review = ReviewShop()
            review.shop = detail_data
            review.user = request.user
            review.score = request.POST['score']
            review.comment = request.POST['comment']
            is_exist = ReviewShop.objects.filter(shop=detail_data.id).filter(user = review.user)
            
            if is_exist:
                messages.error(request, '既にレビューを投稿済みです。') # 追加
                return redirect('shop:detail', detail_data.name) # 追加
            else:
                review.save()
                messages.success(request, 'レビューを投稿しました。') # 追加
                return redirect('shop:detail', detail_data.name)
        else:
            form_data = self.request.session.get('form', form)
            messages.error(self.request, 'エラーがあります。レビューのスコア（５段階）を選択して、コメントを記入してください。')
            return redirect('shop:detail', detail_data.name)
          
        return render(request, 'shop/index.html', {})
        
    
# お気に入りに追加ボタンの処理
@login_required
def Like_shop(request, name):
    shop = Shop.objects.filter(name = name).first()
    is_already = LikeShop.objects.filter(liked_by = request.user, shop = shop.id).count()
    if is_already > 0:
        messages.error(request, '既にお気に入りに追加済みです。')
        return redirect('shop:detail', shop.name)
    
    like_shop = LikeShop()
    like_shop.liked_by = request.user
    like_shop.shop = shop
    like_shop.save()

    messages.success(request, 'お気に入りに追加しました！')
    return redirect('shop:detail', shop.name)


# お気に入りから削除ボタンの処理
@login_required
def Like_shop_delete(request, name):
    shop = Shop.objects.filter(name = name).first()
    like_shop = LikeShop.objects.filter(shop = shop).filter(liked_by = request.user)
    like_shop.delete()

    messages.success(request, 'お気に入りから削除しました')
    return redirect('shop:detail', shop.name)


def OwnerList(request):
    owner_list = User.objects.filter(is_owner = True)
    params = {
        'owner_list': owner_list,
    }
    return render (request, 'shop/owner_list.html', params)

# ShopのCSVインポート/アップロード
def shop_upload(request):
    if 'csv' in request.FILES:
        form_data = TextIOWrapper(request.FILES['csv'].file, encoding='utf-8')
        csv_file = csv.reader(form_data)
        for line in csv_file:
            shop, created = Shop.objects.get_or_create(owner=User.objects.get(username='admin'), pref = Pref.objects.get(name=line[11]), short_content = line[5], content = line[5], views='0')
            shop.shop_url = line[1]
            shop.shop_fb = line[2]
            shop.shop_tw = line[3]
            shop.shop_insta = line[4]
            shop.name = line[5]
            shop.zipcode = line[10]
            shop.address = line[12]
            shop.shop_email = line[13]
            shop.shop_tel = line[14]
            # shop.pref = Pref.objects.get(name=line[11])
            shop.save()

        return render(request, 'shop/upload.html')

    else:
        return render(request, 'shop/upload.html')

# Shopのエクスポート
def shop_export(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="shops.csv"'
    # HttpResponseオブジェクトはファイルっぽいオブジェクトなので、csv.writerにそのまま渡せます。
    writer = csv.writer(response)
    for shop in Shop.objects.all():
        writer.writerow([shop.pk, shop.name, shop.pref, shop.owner])
    return response

# 都道府県別のショップを出すページ
class PrefDetail(DetailView):
    model = Pref
    slug_field = 'name'  # モデルのフィールドの名前
    slug_url_kwarg = 'name'  # urls.pyでのキーワードの名前

    def get_context_data(self, *args, **kwargs):
        pref_name = kwargs['object']
        num = Shop.objects.filter(pref = pref_name).count()
        shop_list = Shop.objects.filter(pref=kwargs['object'])

        params = {
            'pref_name': pref_name,
            'num': num,
            'shop_list': shop_list,
            }
        return params


# 都道府県別のショップを出すページ
class TagDetail(DetailView):
    model = Tag
    slug_field = 'name'  # モデルのフィールドの名前
    slug_url_kwarg = 'name'  # urls.pyでのキーワードの名前

    def get_context_data(self, *args, **kwargs):
        tag_name = kwargs['object']
        shop_list = Shop.objects.filter(tag=kwargs['object'])

        params = {
            'tag_name': tag_name,
            # 'num': num,
            'shop_list': shop_list,
            }
        return params


class ReviewUpdate(OnlyYourReviewMixin, UpdateView):
    model = ReviewShop
    form_class = ReviewForm
    template_name = 'shop/review_update.html'

    # def get_success_url(self):
    #     messages.info(self.request, 'Postを更新しました。')
    #     return resolve_url('myapp:post_detail', pk=self.kwargs['pk'])

    def get_success_url(self):
        messages.success(self.request, 'レビューを更新しました！')
        shopname = ReviewShop.objects.get(id = self.kwargs['pk'])
        return resolve_url('shop:detail', name=shopname)


class ReviewDelete(OnlyYourReviewMixin, DeleteView):
    model = ReviewShop
    template_name = 'shop/review_delete.html'

    def delete(self, request, *args, **kwargs):
        result = super().delete(request, *args, **kwargs)
        messages.success(
            self.request, '「{}」を削除しました'.format(self.object))
        return result

    def get_success_url(self):
        messages.success(self.request, 'レビューを削除しました！')
        shopname = ReviewShop.objects.get(id = self.kwargs['pk'])
        return resolve_url('shop:detail', name=shopname)