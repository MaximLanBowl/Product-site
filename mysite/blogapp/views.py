from django.contrib.auth import views
from django.shortcuts import render
from django.contrib.syndication.views import Feed
from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse, reverse_lazy
from blogapp.models import Article


class ArticlesListView(ListView):
    template_name = "blogapp/article_list.html"
    queryset = (
        Article.objects
        .order_by("-pub_date")
        .select_related("author")
        .prefetch_related("category", "tags")
        .all()
    )


class ArticleDetailView(DetailView):
    model = Article


class ArticleCreateView(CreateView):
    template_name = "blogapp/create_article.html"
    model = Article
    fields = "title", "pub_date", "author", "category", "tags"
    success_url = reverse_lazy("blogapp:article")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ArticlesDetailView(DetailView):
    model = Article


class ArticleLatestFeed(Feed):
    title = "Blog articles (latest)"
    description = "Updates on changes and additions blog articles"
    link = reverse_lazy("blogapp:article")

    def items(self):
        return (
            Article.objects
            .filter(pub_date__isnull=False)
            .order_by("-pub_date")[:5]
        )

    def item_title(self, item: Article):
        return item.title

    def item_description(self, item: Article):
        return item.content[:200]

   