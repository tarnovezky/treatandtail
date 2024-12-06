from django.test import TestCase
from shop.models import Cart, User

class CartModelTest(TestCase):
    def test_only_one_active_cart(self):
        user = User.objects.create(username="testuser")
        Cart.objects.create(user=user, is_active=True)
        cart2 = Cart.objects.create(user=user, is_active=True)

        # Ensure only one active cart exists
        active_carts = Cart.objects.filter(user=user, is_active=True)
        self.assertEqual(active_carts.count(), 1)
        self.assertEqual(active_carts.first(), cart2)
