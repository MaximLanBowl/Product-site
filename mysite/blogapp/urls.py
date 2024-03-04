from django.urls import path

from .views import (
    ArticleCreateView,
    ArticlesListView,
    ArticlesDetailView,
    ArticleLatestFeed,
)

urlpatterns = [
    path('article/create/', ArticleCreateView.as_view(), name="create_art"),
    path('article/', ArticlesListView.as_view(), name="article"),
    path('article/<int:pk>/', ArticlesDetailView.as_view(), name="article-details"),
    path('article/latest/feed/', ArticleLatestFeed(), name="feed"),
]