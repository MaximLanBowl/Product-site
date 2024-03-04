from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.conf import settings

from shopapp.models import Product, Order
from django.urls import reverse
from string import ascii_letters
from random import choices


class ProductCreateViewTestCase(TestCase):
    def setUp(self):
        self.product_name = "".join(choices(ascii_letters, k=10))
        Product.objects.filter(name=self.product_name).delete()

    def test_create_product(self):
        response = self.client.post(reverse("shopapp:create_product"),
                                    {
                                        "name": self.product_name,
                                        "price": "300.00",
                                        "description": "Top",
                                        "discount": "10",
                                    }
                                    )
        self.assertRedirects(response, reverse("shopapp:products_list"))
        self.assertTrue(Product.objects.filter(name=self.product_name).exists())


class ProductDetailsViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.product = Product.objects.create(name="Best Product")

    @classmethod
    def tearDownClass(cls):
        cls.product.delete()

    def test_get_product(self):
        response = self.client.get(
            reverse
            ("shopapp:product_details",
             kwargs={"pk": self.product.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_get_product_and_check_content(self):
        response = self.client.get(
            reverse
            ("shopapp:product_details",
             kwargs={"pk": self.product.pk})
        )
        self.assertContains(response, self.product.name)


class ProductsListViewTestCase(TestCase):
    fixtures = [
        'products-fixture.json',
    ]

    def test_products(self):
        response = self.client.get(reverse('shopapp:products_list'))
        self.assertQuerysetEqual(
            qs=Product.objects.filter(archive=False).all(),
            values=(p.pk for p in response.context["products"]),
            transform=lambda p: p.pk,
        )
        self.assertTemplateUsed(response, template_name='shopapp/products-list.html')


class OrdersListViewTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.credentials = dict(username="bob_test", password="qwerty")
        cls.user = User.objects.create_user(**cls.credentials)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self):
        self.client.force_login(self.user)

    def test_orders_view(self):
        response = self.client.get(reverse("shopapp:orders_list"))
        self.assertContains(response, "Orders")

    def test_orders_view_not_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse("shopapp:orders_list"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(str(settings.LOGIN_URL), response.url)


class OrderDetailsViewTestCase(TestCase):
    user = None

    @classmethod
    def setUpClass(cls):
        cls.user = (User.objects.create_user
                    (username="admin",
                     password="qwerty123")
                    )
        permission_order = Permission.objects.get(codename="view_order")
        cls.user.user_permissions.add(permission_order)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self):
        self.client.force_login(self.user)
        self.order = Order.objects.create(
            delivery_adress='De',
            promocode='wert',
            user=self.user
        )

    def tearDown(self):
        self.order.delete()

    def test_order_details(self):
        response = self.client.get(reverse(
            'shopapp:order_details',
            kwargs={'pk': self.order.pk})
        )
        self.assertContains(response, self.order.delivery_adress)
        self.assertContains(response, self.order.promocode)
        received_data = response.context["order"].pk
        expected_data = self.order.pk
        self.assertEqual(received_data, expected_data)


class ProductsExportViewTestCase(TestCase):
    fixtures = [
        'products-fixture.json'
    ]

    def test_get_products_view(self):
        response = self.client.get(
            reverse("shopapp:products-export"),
        )
        self.assertEqual(response.status_code, 200)
        products = Product.objects.order_by("pk").all()
        expected_data = [
            {
                "pk": product.pk,
                "name": product.name,
                "price": str(product.price),
                "archive": product.archive,
            }
            for product in products
        ]
        products_data = response.json()
        self.assertEqual(
            products_data["products"],
            expected_data,
        )


class OrdersExportTestCase(TestCase):
    fixtures = [
        'orders-fixture.json',
    ]

    @classmethod
    def setUpClass(cls):
        cls.user = (User.objects.create_user
                    (username="maxim",
                     password="qwerty123")
                    )

        permission_order = Permission.objects.get(codename="view_order")
        cls.user.user_permissions.add(permission_order)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self):
        self.client.force_login(self.user)

    def test_get_orders_view(self):
        response = self.client.get(
            reverse("shopapp:orders-export")
        )
        self.assertEqual(response.status_code, 200)
        orders = Order.objects.order_by("pk").all()
        expected_data = [
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
            for order in orders
        ]
        self.assertEqual(response.status_code, 200)
        orders_data = response.json()
        self.assertEqual(
            orders_data["orders"],
            expected_data,
        )
