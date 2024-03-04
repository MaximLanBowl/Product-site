from django.contrib import admin
from .models import Author, Tag, Article, Category



admin.site.register(Author)
admin.site.register(Article)
admin.site.register(Tag)
admin.site.register(Category)

