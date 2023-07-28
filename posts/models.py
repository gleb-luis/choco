from django.db import models
from accounts.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Avg


# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(
        'accounts.User', on_delete=models.CASCADE)
    picture = models.ImageField(
        upload_to="image/posts/", blank=False, null=False)
    text = models.TextField(blank=True)
    country = models.ForeignKey('Country', on_delete=models.PROTECT)
    taste = models.ForeignKey('posts.Taste', on_delete=models.PROTECT)
    cacao = models.PositiveSmallIntegerField('カカオ含有率', validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)
    views = models.PositiveIntegerField('アクセス数', default=0)
    # average_score = models.FloatField('平均スコア', default=0)
    # review_count = models.PositiveIntegerField('レビュー数', default=0)
    gained_like = models.PositiveIntegerField('獲得したLike数', default=0)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.text)

    def get_review_count(self):
        review_count = Review.objects.filter(post=self).count()
        return review_count

    def get_average_score(self):
        average_score = Review.objects.filter(post=self).aggregate(Avg('score'))
        return average_score['score__avg']

    def get_percent(self):
        percent = round(self.average_score / 5 * 100)
        return percent

    def get_like_count(self):
        like_count = Like.objects.filter(post=self).count()
        return like_count

class Like(models.Model):
    liked_by = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE)


class Country(models.Model):
    country = models.CharField('原産国', max_length=255)
    def __str__(self):
        return str(self.country)

class Taste(models.Model):
    taste = models.CharField('テイスト', max_length=122)
    def __str__(self):
        return str(self.taste)


SCORE_CHOICES = [
    (1, '★'),
    (2, '★★'),
    (3, '★★★'),
    (4, '★★★★'),
    (5, '★★★★★'),
]

class Review(models.Model):
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE)
    user = models.ForeignKey('accounts.User', on_delete=models.PROTECT)
    comment = models.TextField(verbose_name='レビューコメント', blank=False)
    score = models.PositiveSmallIntegerField(verbose_name='レビュースコア', choices=SCORE_CHOICES, default='3')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('post', 'user')

    def __str__(self):
        return str(self.post)

    def get_percent(self):
        percent = round(self.score / 5 * 100)
        return percent