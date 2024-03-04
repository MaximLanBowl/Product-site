from django.db import models
from django.urls import reverse
from django.utils import timezone


class Author(models.Model):
    """
    Модель Author представляет автора статьи,
    который описывает свою биографию
    """
    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"

    name = models.CharField(max_length=100, db_index=True)
    bio = models.TextField(max_length=100)

    def authorname(self):
        return self.authorname(name=self.name)



class Category(models.Model):
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=40, db_index=True)


class Tag(models.Model):
    name = models.CharField(max_length=20, db_index=True)


class Article(models.Model):
    objects = None
    title = models.CharField(max_length=200)
    content = models.TextField(null=False, max_length=100)
    pub_date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name="tags", blank=True)

    def get_absolute_url(self):
        return reverse("blogapp:article-details", kwargs={"pk": self.pk})
