from django.db import models

# Create your models here.


class NBANews(models.Model):
    title = models.CharField(max_length=200)
    img_url = models.CharField(max_length=200)
    detail_url = models.CharField(max_length=200)
    paragraph = models.TextField()   # 有換行符號
    datetime = models.CharField(max_length=200)


class NBANewsDetail(models.Model):
    nba_news = models.ForeignKey(NBANews, on_delete=models.CASCADE)
    detail_title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    paragraph = models.TextField()     # rich text
