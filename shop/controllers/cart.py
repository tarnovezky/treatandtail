from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from shop.models import Product, Cart, CartItem, ProductFlavor
import json
from django.views.decorators.csrf import csrf_exempt


class CartManager:
    """Manages user and guest cart operations."""

    def __init__(self, request):
        self.request = request

    def get_cart(self):
        """Retrieve or create a cart for authenticated or guest users."""
        if self.request.user.is_authenticated:
            # Get or create cart for logged-in user
            cart, _ = Cart.objects.get_or_create(user=self.request.user, is_active=True)
        else:
            # Get or create cart for session
            session_key = self.request.session.session_key
            if not session_key:
                self.request.session.create()
                session_key = self.request.session.session_key
            cart, _ = Cart.objects.get_or_create(session_key=session_key, is_active=True)
        return cart

    def merge_carts(self):
        """
        Merge session cart into user's cart upon login.
        """
        if not self.request.user.is_authenticated:
            return

        session_key = self.request.session.session_key
        if not session_key:
            return

        # Get session-based cart
        session_cart = Cart.objects.filter(session_key=session_key, is_active=True).first()

        # Get user-based cart
        user_cart, _ = Cart.objects.get_or_create(user=self.request.user, is_active=True)

        if session_cart and session_cart != user_cart:
            # Merge items from session cart to user cart
            for item in session_cart.items.all():
                existing_item = user_cart.items.filter(product=item.product, flavor=item.flavor).first()
                if existing_item:
                    existing_item.quantity += item.quantity
                    existing_item.save()
                else:
                    item.cart = user_cart
                    item.save()

            # Deactivate the session cart
            session_cart.delete()



    def add_to_cart(self, product_id, flavor_id=None, quantity=1):
        """Add a product to the cart."""
        product = get_object_or_404(Product, id=product_id)
        flavor = get_object_or_404(ProductFlavor, id=flavor_id) if flavor_id else None
        cart = self.get_cart()

        # Get or create a cart item
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, flavor=flavor)
        if created:
            cart_item.quantity = quantity
        else:
            cart_item.quantity += quantity
        cart_item.save()

        return JsonResponse({
            "success": True,
            "message": f"{product.name} ({flavor.flavor_name if flavor else 'Default'}) added to cart.",
            "total_items": cart.num_of_items,
            "cart_item_quantity": cart_item.quantity,
            "selected_flavor": flavor.flavor_name if flavor else "No Flavor"
        })

    def update_quantity(self, item_id, action):
        """Update the quantity of a cart item."""
        cart = self.get_cart()
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        if action == 'increase':
            cart_item.quantity += 1
        elif action == 'decrease':
            cart_item.quantity -= 1
            if cart_item.quantity < 1:
                cart_item.delete()
                return JsonResponse({
                    'success': True,
                    'item_removed': True,
                    'cart_total_price': cart.total_price
                })
        cart_item.save()

        return JsonResponse({
            'success': True,
            'new_quantity': cart_item.quantity,
            'item_total_price': cart_item.total_price,
            'cart_total_price': cart.total_price
        })

    def clear_cart(self):
        """Clear all items in the cart."""
        cart = self.get_cart()
        if cart:
            cart.items.all().delete()
            return redirect('cart')
        return JsonResponse({'error': 'Cart not found'}, status=404)

    def remove_cart_item(self, item_id):
        """Remove a single item from the cart."""
        cart = self.get_cart()
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        cart_item.delete()
        return redirect('cart')

    def get_cart_items(self):
        """Retrieve all items in the cart."""
        cart = self.get_cart()
        return cart.items.all()


# Cart-related views
@csrf_exempt
def add_to_cart(request):
    """Add an item to the cart."""
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            product_id = body.get('id')
            flavor_id = body.get('flavor')
            quantity = int(body.get('quantity', 1))
            manager = CartManager(request)
            return manager.add_to_cart(product_id, flavor_id, quantity)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method."}, status=400)


@csrf_exempt
def update_quantity(request):
    """Update the quantity of a cart item."""
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            item_id = body.get('item_id')
            action = body.get('action')
            manager = CartManager(request)
            return manager.update_quantity(item_id, action)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=400)


def clear_cart(request):
    """Clear all items from the cart."""
    manager = CartManager(request)
    return manager.clear_cart()


def remove_cart_item(request, item_id):
    """Remove a single item from the cart."""
    manager = CartManager(request)
    return manager.remove_cart_item(item_id)
