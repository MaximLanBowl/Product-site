from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.views.decorators.cache import cache_page

from .views import (
    ShopIndexView,
    GroupsListView,
    ProductDetailsView,
    ProductsListView,
    ProductUpdateView,
    OrdersListView,
    OrderDetailsView,
    OrderUpdateView,
    ProductDeleteView,
    OrderDeleteView,
    OrderCreateView,
    ProductCreateView,
    OrdersDataExportView,
    ProductsDataExportView,
    ProductViewSet,
    OrderViewSet,
    LatestProductsFeed, UserOrdersListView, ExportUserOrders,
)

app_name = "shopapp"

routers = DefaultRouter()
routers.register("products", ProductViewSet)
routers.register("orders", OrderViewSet)

urlpatterns = [
    # path("", cache_page(60)(ShopIndexView.as_view()), name="index"),
    path("", ShopIndexView.as_view(), name="index"),
    path("api/", include(routers.urls)),
    path("groups/", GroupsListView.as_view(), name='groups_list'),
    path("products/", ProductsListView.as_view(), name="products_list"),
    path("products/export/", ProductsDataExportView.as_view(), name="products-export"),
    path("products/create/", ProductCreateView.as_view(), name='create_product'),
    path("products/<int:pk>", ProductDetailsView.as_view(), name='product_details'),
    path("products/<int:pk>/update", ProductUpdateView.as_view(), name='product_update'),
    path("products/<int:pk>/archive", ProductDeleteView.as_view(), name='product_delete'),
    path("products/latest/feed", LatestProductsFeed(), name='products_feed'),
    path("orders/", OrdersListView.as_view(), name='orders_list'),
    path("orders/export/", OrdersDataExportView.as_view(), name='orders-export'),
    path("orders/create/", OrderCreateView.as_view(), name='create_order'),
    path("order/<int:pk>", OrderDetailsView.as_view(), name='order_details'),
    path("order/<int:pk>/update", OrderUpdateView.as_view(), name='order_update'),
    path("order/<int:pk>/archive", OrderDeleteView.as_view(), name='order_delete'),
    path("users/<int:user_id>/orders/", UserOrdersListView.as_view(), name="user_orders_list"),
    path("users/<int:user_id>/orders/export/", ExportUserOrders.as_view(), name="user_export_orders"),
]
