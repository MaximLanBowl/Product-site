"""
В этом модуле лежат различные наборы представлений.

Разные view интернет-магазина: по товарам, заказам и т.д.
"""

from csv import DictWriter
import logging
from django.contrib.auth.models import Group
from django.contrib.syndication.views import Feed
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.core.cache import cache

from django.http import (HttpResponse, HttpRequest,
                         HttpResponseRedirect, JsonResponse)

from timeit import default_timer

from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.decorators.cache import cache_page
from django.views.generic import (DeleteView, ListView,
                                  DetailView, CreateView, UpdateView)

from drf_spectacular.utils import extend_schema, OpenApiResponse

from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.request import Request
from rest_framework.response import Response

from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from .models import User

from .common import save_csv_products
from .models import Product, Order, ProductImage
from .forms import GroupForm, ProductForm
from django.views import View
from .serializers import ProductSerializer, OrderSerializer
from django.utils.decorators import method_decorator

log = logging.getLogger(__name__)


@extend_schema(description="Product view CRUD")
class ProductViewSet(ModelViewSet):
    """
    Набор представлений для действий над Product
    <br>
    Полный CRUD для сущностей товара
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]

    search_fields = ["name", "description"]

    filterset_fields = [
        "name",
        "description",
        "price",
        "discount",
        "archive"
    ]

    ordering_fields = [
        "name",
        "price",
        "discount",
    ]

    @method_decorator(cache_page(60))
    def list(self, *args, **kwargs):
        print("hello products list")
        return super().list(*args, **kwargs)

    @extend_schema(
        summary="Get one product by ID",
        description="Retrieves **product**, return 404 if not page found",
        responses={
            200: ProductSerializer,
            404: OpenApiResponse(description="Empty responce, product by id not found"),
        }
    )
    def retrieve(self, *args, **kwargs):
        return super().request(*args, **kwargs)

    @action(methods=["get"], detail=False)
    def download_csv(self, request: Request):
        response = HttpResponse(content_type="text/csv")
        filename = "products-export.csv"
        response["Content-Disposition"] = f"attachment; filename={filename}"
        queryset = self.filter_queryset(self.get_queryset())
        fields = [
            "name",
            "description",
            "price",
            "discount"
        ]
        queryset = queryset.only(*fields)
        writer = DictWriter(response, fieldnames=fields)
        writer.writeheader()

        for product in queryset:
            writer.writerow({
                field: getattr(product, field)
                for field in fields
            })
        return response

    @action(
        detail=False,
        methods=["post"],
        parser_classes=[MultiPartParser]
    )
    def upload_csv(self, request: Request):
        products = save_csv_products(
            request.FILES["file"].file,
            encoding=request.encoding,
        )
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter,
    ]

    filterset_fields = [
        "user",
        "products",
        "delivery_adress",
        "created_at",
    ]

    ordering_fields = [
        "user",
        "products",
        "delivery_adress",
    ]


class ShopIndexView(View):
    # @method_decorator(cache_page(60))
    def get(self, request: HttpRequest) -> HttpResponse:
        products = [
            ('Laptop', 1999),
            ('Desktop', 2999),
            ('Smartphone', 999),
        ]
        context = {
            "time_run": default_timer().__round__(2),
            "products": products,
            "items": 1,
        }
        log.debug("Products for shop index: %s", products)
        log.info("Rendering shop index")
        print(f"shop index context {context}")
        return render(request, 'shopapp/shop-index.html', context=context)


class GroupsListView(View):
    def get(self, request: HttpRequest):
        context = {
            "form": GroupForm(),
            "groups": Group.objects.prefetch_related("permissions").all(),
        }
        return render(request, 'shopapp/groups-list.html', context=context)

    def post(self, request: HttpRequest):
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(request.path)


class ProductsListView(ListView):
    # model = Product
    template_name = 'shopapp/products-list.html'
    context_object_name = "products"
    queryset = Product.objects.filter(archive=False)


class ProductDetailsView(DetailView):
    template_name = 'shopapp/products-details.html'
    # model = Product
    queryset = Product.objects.prefetch_related("images")
    context_object_name = "product"


class ProductUpdateView(UpdateView):
    template_name = "shopapp/product_form_update.html"
    model = Product
    # fields = "name", "price", "description", "discount", "preview"
    form_class = ProductForm

    def get_success_url(self):
        return reverse(
            "shopapp:product_details",
            kwargs={"pk": self.object.pk},
        )

    def form_valid(self, form):
        response = super().form_valid(form)
        for image in form.files.getlist("images"):
            ProductImage.objects.create(
                product=self.object,
                image=image,
            )
        return response


class ProductCreateView(PermissionRequiredMixin, CreateView):

    def test_func(self):
        return self.request.user.is_superuser

    permission_required = "shopapp.change_product"
    model = Product
    fields = "name", "price", "description", "discount", "preview"
    success_url = reverse_lazy("shopapp:products_list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("shopapp:products_list")

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archive = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class LatestProductsFeed(Feed):
    name = "Shop products (latest)"
    description = "Updates on changes and additions shop products"
    link = reverse_lazy("shopapp:products")

    def items(self):
        return (
            Product.objects
            .filter(creat_at__isnull=False)
            .order_by("-create_at")[:5]
        )

    def item_title(self, item: Product):
        return item.name

    def item_description(self, item: Product):
        return item.description[:200]


class OrderDetailsView(PermissionRequiredMixin, DetailView):
    permission_required = "shopapp.view_order"
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
    )


class OrderUpdateView(UpdateView):
    model = Order
    fields = ["user", "products"]

    def get_success_url(self):
        return reverse(
            "shopapp:order_details",
            kwargs={"pk": self.object.pk},
        )


class OrdersListView(LoginRequiredMixin, ListView):
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
        .filter(archive=False)
    )


class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy("shopapp:orders_list")

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archive = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class OrderCreateView(CreateView):
    model = Order
    fields = "user", "products", "delivery_adress", "promocode"
    success_url = reverse_lazy("shopapp:orders_list")


class ProductsDataExportView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        cache_key = "products_data_export"
        products_data = cache.get(cache_key)
        if products_data is None:
            products = Product.objects.order_by("pk").all()
            products_data = [
                {
                    "pk": product.pk,
                    "name": product.name,
                    "price": product.price,
                    "archive": product.archive,
                }
                for product in products
            ]

        elem = products_data[0]
        name = elem["name"]
        print("name:", name)
        cache.set("products_data_export", products_data, 300)
        return JsonResponse({"products": products_data})


class OrdersDataExportView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        orders = Order.objects.order_by("pk").all()
        orders_data = [
            {
                "pk": order.pk,
                "delivery_adress": order.delivery_adress,
                "promocode": order.promocode,
                "created_at": order.created_at,
                "user": order.user.id,
                "archive": order.archive,
                "products": [
                    order.product.id
                ]
            }
            for order in orders]
        return JsonResponse({"orders": orders_data})


class ExportUserOrders(View):
    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)

        cache_key = f"users_orders_{user_id}"
        cached_data = cache.get(cache_key)

        if cached_data:
            return JsonResponse(cached_data)

        orders = Order.objects.filter(user=user).order_by('pk')
        serializer = OrderSerializer(orders, many=True)
        data = serializer.data

        cache.set(cache_key, data, timeout=120)

        return JsonResponse(data, safe=False)


class UserOrdersListView(LoginRequiredMixin, ListView):
    model = Order
    owner = None

    def get_queryset(self):
        owner: User = get_object_or_404(User, pk=self.kwargs["user_id"])
        queryset = super().get_queryset()
        queryset = (
            queryset
            .select_related("user")
            .prefetch_related("products")
            .order_by("pk")
            .filter(user=owner)
            .all()
        )
        self.owner = owner
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update(owner=self.owner)
        return context
