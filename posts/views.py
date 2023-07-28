from django.shortcuts import render, redirect, resolve_url
from django.views import generic
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views import  View 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .forms import PostForm, SearchForm, ReviewForm
from .models import Post, Like, Country, Taste, Review
from column.models import Column
from django.contrib import messages
from django.db.models import Q
from django.db.models import Avg


class OnlyYourPostMixin(UserPassesTestMixin):
    raise_exception = True
    # 自分がオーナーのPostのみ
    def test_func(self):
        post = Post.objects.get(id = self.kwargs['pk'])
        return post.author == self.request.user


class Create(CreateView):
    template_name = 'posts/create.html'
    form_class = PostForm
    success_url = reverse_lazy('posts:index')

    # 入力に問題がない場合現在ログインしているアカウントを投稿者として登録するための処理
    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        return super(Create, self).form_valid(form)


class Index(ListView):
    model = Post
    template_name = 'posts/index.html'
    paginate_by = 100

    def get_context_data(self, *args, **kwargs):
        searchform = SearchForm()
        post_list = Post.objects.order_by('-created_at')
        column_list = Column.objects.order_by('-created_at')[:6]
        params = {
            'searchform': searchform,
            'post_list': post_list,
            'column_list': column_list,
            }
        return params


class Update(OnlyYourPostMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/update.html'

    def get_success_url(self):
        messages.success(self.request, '更新しました！')
        return resolve_url('posts:detail', pk=self.kwargs['pk'])


class Delete(OnlyYourPostMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('posts:index')
    template_name = 'posts/delete.html'

    def delete(self, request, *args, **kwargs):
        result = super().delete(request, *args, **kwargs)
        messages.success(
            self.request, '「{}」を削除しました'.format(self.object))
        return result


def Search(request):
    if request.method == 'GET':
        form = SearchForm(request.GET)

        if form.is_valid():
            # selected_country = form.cleaned_data['selected_country']

            # selected_country =  request.GET.get('selected_country')
            
            # selected_country = Country.objects.get(id = 1)

            # selected_country = Country.objects.get(country = request.GET.get('selected_country')) #これはエラーになる
            # selected_country = Country.objects.get(country = form.cleaned_data['selected_country']) #これはエラーになる
            
            # selected_taste = form.cleaned_data['selected_taste']
            # selected_taste =  request.GET.get('selected_taste')
            
            freeword = form.cleaned_data['freeword']
            # search_list = Post.objects.filter(Q(text__icontains=freeword)|Q(country__country=selected_country)|Q(taste__taste=selected_taste))
            search_list = Post.objects.filter(Q(text__icontains=freeword))

    params = {
        'post_list': search_list,
        'freeword': freeword,
        # 'selected_country': selected_country,
        }

    return render (request, 'posts/search.html', params)



def Detail(request, pk):
    detail_data = Post.objects.get(id = pk)#getにすることでオブジェクトを取得。filterだとQueryを取得になってしまう。
    detail_data.views += 1 #アクセス数をいったんカウントアップして保存
    detail_data.save()
    users_post_list = Post.objects.filter(author = detail_data.author)
    average_score = Review.objects.filter(post=pk).aggregate(Avg('score'))
    average = average_score['score__avg']
    if average:
        average_rate = average / 5 * 100
    else:
        average_rate = 0

    if request.method == 'GET':
        review_form = ReviewForm()
        review_list = Review.objects.filter(post=pk)
        detail_data.save()
    else:
        form = ReviewForm(data=request.POST)
        score = request.POST['score']
        comment = request.POST['comment']

        if form.is_valid():
            review = Review()
            review.post = detail_data
            review.user = request.user
            review.score = score
            review.comment = comment

            is_exist = 0
            is_exist = Review.objects.filter(post=pk).filter(user = review.user).count()
            
            if not is_exist == 0:
                messages.error(request, '既にレビューを投稿済みです。') # 追加
                return redirect('posts:detail', pk) # 追加
            else:
                review.save()
                messages.success(request, 'レビューを投稿しました。') # 追加
                return redirect('posts:detail', pk)
        else:
            messages.error(request, 'エラーがあります。') # 追加
            return redirect('posts:detail', pk)
        return render(request, 'posts/index.html', {})

    params = {
        'object': detail_data,
        'review_form': review_form,
        'review_list': review_list,
        'average_rate': average_rate,
        'users_post_list': users_post_list,
        }

    return render (request, 'posts/detail.html', params)


class CountryDetail(DetailView):
    model = Country
    slug_field = 'country'  # モデルのフィールドの名前
    slug_url_kwarg = 'country'  # urls.pyでのキーワードの名前

    def get_context_data(self, *args, **kwargs):
        country_name = kwargs['object']
        num = Post.objects.filter(country = country_name).count()
        post_list = Post.objects.filter(country=kwargs['object']).order_by('-updated_at')

        params = {
            'country_name': country_name,
            'num': num,
            'post_list': post_list,
            }
        return params


class TasteDetail(DetailView):
    model = Taste
    slug_field = 'taste'  # モデルのフィールドの名前
    slug_url_kwarg = 'taste'  # urls.pyでのキーワードの名前

    def get_context_data(self, *args, **kwargs):
        taste_name = kwargs['object']
        num = Post.objects.filter(taste = taste_name).count()
        post_list = Post.objects.filter(taste=kwargs['object']).order_by('-updated_at')

        params = {
            'taste_name': taste_name,
            'num': num,
            'post_list': post_list,
            }
        return params

# 以下はビューではなく処理の関数
# LIKEボタンの処理
@login_required
def like(request, post_id):
    like_post = Post.objects.get(id=post_id)
    is_liked = Like.objects.filter(liked_by = request.user).filter(post=like_post).count()
    if is_liked > 0:
        messages.error(request, '既に「いいね！」をしています。')
        return redirect('posts:index')#ページ遷移をしないのはこれでいいか？    
    like = Like()
    like.liked_by = request.user
    like.post = like_post
    like.save()

    like_post.gained_like += 1
    like_post.save()

    messages.success(request, '「いいね！」しました！')
    return redirect('posts:index')

