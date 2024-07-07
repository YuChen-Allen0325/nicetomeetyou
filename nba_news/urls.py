from django.urls import path, include
from . import views


urlpatterns = [
    path('nba_news/', views.NBANewsView.as_view(), name='nba_news'),
    path('nba_news_detail/', views.NBANewsDetailView.as_view(), name='nba_news_detail'),
    path('cron_job/', views.CronJobView.as_view(), name='cron_job'),
]
