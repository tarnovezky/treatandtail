from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from shop.models import Product, UserAdditionalInfo, Cart
User = get_user_model()
class ProductListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        Product.objects.create(name="Test Product 1", slug="test-product-1", article="TP123")
        Product.objects.create(name="Test Product 2", slug="test-product-2", article="TP124")

    def test_product_list_view(self):
        response = self.client.get(reverse('shop:product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Product 1")
        self.assertContains(response, "Test Product 2")

class ProductDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.product = Product.objects.create(name="Test Product", slug="test-product", article="TP123")

    def test_product_detail_view(self):
        response = self.client.get(reverse('shop:product_detail', kwargs={'slug': self.product.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

class CartPageViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.cart = Cart.objects.create(user=self.user, is_active=True)

    def test_cart_page_authenticated_user(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse('shop:cart_page'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Cart")
