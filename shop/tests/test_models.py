from django.test import TestCase
from django.contrib.auth import get_user_model
from shop.models import UserAdditionalInfo, Tag, Product, ProductFlavor, Cart, CartItem, Order, Review, Comment

User = get_user_model()

class UserAdditionalInfoTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", email="testuser@example.com")
        self.additional_info = UserAdditionalInfo.objects.create(user=self.user, phone="1234567890", roles="customer")

    def test_user_additional_info_creation(self):
        self.assertEqual(self.additional_info.user.username, "testuser")
        self.assertEqual(self.additional_info.roles, "customer")
        self.assertEqual(self.additional_info.phone, "1234567890")

    def test_roles_required(self):
        with self.assertRaises(ValueError):
            UserAdditionalInfo.objects.create(user=self.user, roles=None)

class ProductModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name="Test Product", slug="test-product", article="TP123", rating=4.5)

    def test_product_rating_validation(self):
        self.assertGreaterEqual(self.product.rating, 0)
        self.assertLessEqual(self.product.rating, 5)

class CartTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.cart = Cart.objects.create(user=self.user, is_active=True)

    def test_single_active_cart(self):
        new_cart = Cart.objects.create(user=self.user, is_active=True)
        self.cart.refresh_from_db()
        self.assertFalse(self.cart.is_active)
        self.assertTrue(new_cart.is_active)

class CartItemTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.cart = Cart.objects.create(user=self.user, is_active=True)
        self.product = Product.objects.create(name="Test Product", slug="test-product", article="TP123")
        self.flavor = ProductFlavor.objects.create(product=self.product, flavor_name="Vanilla", price=10.0)
        self.cart_item = CartItem.objects.create(cart=self.cart, product=self.product, flavor=self.flavor, quantity=2)

    def test_cart_item_total_price(self):
        self.assertEqual(self.cart_item.total_price, 20.0)
