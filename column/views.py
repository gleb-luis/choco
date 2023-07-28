from django.shortcuts import render, resolve_url
from django.views import generic
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views import  View 
from .forms import ColumnForm
from .models import Column
from accounts.models import User
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404


class OnlyYourColumnMixin(UserPassesTestMixin):
    raise_exception = True
    # 自分がオーナーのColumnのみ
    def test_func(self):
        column = Column.objects.get(id = self.kwargs['pk'])
        return column.author == self.request.user


class Create(CreateView):
    template_name = 'column/create.html'
    form_class = ColumnForm
    success_url = reverse_lazy('column:index')

    # 入力に問題がない場合現在ログインしているアカウントを投稿者として登録するための処理
    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        return super(Create, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, '新しいコラムを投稿しました！')
        return resolve_url('shop:index')


class Index(ListView):
    model = Column
    template_name = 'column/index.html'
    paginate_by = 12

    def get_queryset(self):
        return Column.objects.filter(is_draft=False).order_by('created_at').reverse()
  

class Update(OnlyYourColumnMixin, UpdateView):
    model = Column
    form_class = ColumnForm
    template_name = 'column/update.html'

    def get_success_url(self):
        messages.success(self.request, 'コラムを更新しました！')
        return resolve_url('column:detail', pk=self.kwargs['pk'])


class Delete(OnlyYourColumnMixin, DeleteView):
    model = Column
    success_url = reverse_lazy('column:index')
    template_name = 'column/delete.html'

    def delete(self, request, *args, **kwargs):
        result = super().delete(request, *args, **kwargs)
        messages.success(
            self.request, '「{}」を削除しました'.format(self.object))
        return result


class Detail(DetailView):
    model = Column
    def get(self, request, *args, **kwargs):
        column = Column.objects.get(id = kwargs['pk'])
        users_column_list = Column.objects.filter(author = column.author).filter(is_draft=False).order_by('-created_at')[:5]
        popular_column_list = Column.objects.filter(is_draft=False).order_by('-views')[:5]
        column.views += 1 #　アクセス数をカウントUPしていったん保存。
        column.save()
        params = {
            'object': column,
            'users_column_list': users_column_list,
            'popular_column_list': popular_column_list,
        }

        return render(request, 'column/detail.html', params)


def Columnist(request):
    columnist = User.objects.filter(is_columnist = True)
    params = {
        'columnist': columnist,
    }
    return render (request, 'column/columnist.html', params)


class MyColumn(ListView):
    model = Column
    template_name = 'column/mycolumn.html'
    paginate_by = 12

    def get_queryset(self):
        return Column.objects.filter(author=self.request.user).order_by('created_at').reverse()