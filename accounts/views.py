from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib import messages
from .forms import SignUpForm, MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm
from .models import User, Follow
from posts.models import Post, Like
from column.models import Column
from shop.models import Shop


class OnlyYouMixin(UserPassesTestMixin):
    raise_exception = True
 # 今ログインしてるユーザーのpkと、そのユーザー情報ページのpkが同じなら許可
    def test_func(self):
        user = self.request.user
        return user.username == self.kwargs['username']


# サインアップ画面
class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'registration/signup.html'

    def get_success_url(self):
        form = self.get_form()
        user = User.objects.get(username=form.data.get('username'))

        login(self.request, user)
        return reverse(
            'accounts:userDetail',
            kwargs={'username': user.username })


class Detail(DetailView):
    model = User
    # urlのパスクエリを引数に取る(後述)
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        this_user = get_object_or_404(User, username=self.kwargs.get("username"))
        post_list = Post.objects.filter(author = this_user).order_by('-created_at')[:6]
        column_list = Column.objects.filter(author = this_user).filter(is_draft=False).order_by('-created_at')
        shop_list = Shop.objects.filter(owner = this_user)
        liked_post = Like.objects.filter(liked_by = this_user)
        liked_post_list = []
        for item in liked_post:
            liked = Post.objects.filter(id=item.post.id)
            liked_post_list.append(liked)

        params = {
            'this_user': this_user,
            'shop_list': shop_list,
            'post_list': post_list,
            'column_list': column_list,
            'liked_post_list': liked_post_list,
            'liked_post': liked_post,
        }

        return params


class Update(OnlyYouMixin, UpdateView):
    model = User
    template_name = 'accounts/update.html'
    fields = ['profile', 'nickname', 'email', 'icon', 'fb', 'tw', 'insta']

    def get_object(self):
        # ログイン中のユーザーで検索することを明示する
        return self.request.user

    def get_success_url(self):
        form = self.get_form()
        return reverse(
            'accounts:detail',
            kwargs={'username': self.request.user.username})

    
@login_required
def follow(request, user_id):
    followee = User.objects.get(id = user_id)
    is_exist = Follow.objects.filter(follower = request.user).filter(followee=user_id).count()
    if is_exist > 0:
        messages.error(request, '既にフォロー済みです。')
        return redirect('shop:index')
    
    follow = Follow()
    follow.followee = user_id
    follow.follower = request.user
    follow.save()

    followee.follower_count += 1
    followee.save()

    messages.success(request, 'フォローしました！')
    return redirect('shop:index')


class PasswordChange(LoginRequiredMixin, PasswordChangeView):
    """パスワード変更ビュー"""
    form_class = MyPasswordChangeForm
    success_url = reverse_lazy('accounts:password_change_done')
    template_name = 'registration/password_change.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # 継承元のメソッドCALL
        context["form_name"] = "password_change"
        return context
    
    
class PasswordChangeDone(PasswordChangeDoneView):
    """パスワード変更しました"""
    template_name = 'registration/password_change_done.html'
    
    
class PasswordReset(PasswordResetView):
    """パスワード変更用URLの送付ページ"""
    subject_template_name = 'mail_template/password_reset/subject.txt'
    email_template_name = 'mail_template/password_reset/message.txt'
    template_name = 'registration/password_reset_form.html'
    form_class = MyPasswordResetForm
    success_url = reverse_lazy('accounts:password_reset_done')


class PasswordResetDone(PasswordResetDoneView):
    """パスワード変更用URLを送りましたページ"""
    template_name = 'registration/password_reset_done.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    """新パスワード入力ページ"""
    form_class = MySetPasswordForm
    success_url = reverse_lazy('accounts:password_reset_complete')
    template_name = 'registration/password_reset_confirm.html'


class PasswordResetComplete(PasswordResetCompleteView):
    """新パスワード設定しましたページ"""
    template_name = 'registration/password_reset_complete.html'