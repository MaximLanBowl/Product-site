from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Product


class ShopSiteMap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Product.objects.filter(create_at__isnull=False).order_by("-create_at")

    def lastmod(self, obj: Product):
        return obj.create_at

    def item_link(self, item: Product):
        return reverse("shopapp:product_details", kwargs={"pk": item.pk})
