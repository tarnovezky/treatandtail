
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from django.shortcuts import get_object_or_404, redirect
from shop.models import Product, Cart, CartItem, ProductFlavor

class CartManager:
    """Manages user cart operations."""

    def __init__(self, request):
        self.request = request

    def get_cart(self):
        if self.request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=self.request.user, is_active=True)
            return cart
        return None

    def add_to_cart(self, product_id, flavor_id=None, quantity=1):
        if not self.request.user.is_authenticated:
            return JsonResponse({"error": "User not authenticated"}, status=401)

        product = get_object_or_404(Product, id=product_id)
        flavor = get_object_or_404(ProductFlavor, id=flavor_id) if flavor_id else None
        cart = self.get_cart()

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, flavor=flavor)
        if created:
            cart_item.quantity = quantity
        else:
            cart_item.quantity += quantity
        cart_item.save()

        return JsonResponse({
            "success": True,
            "message": f"{product.name} ({flavor.flavor_name if flavor else 'Default'}) added to cart.",
            "total_items": cart.items.count(),
            "cart_item_quantity": cart_item.quantity,
            "selected_flavor": flavor.flavor_name if flavor else "No Flavor"
        })

    def update_quantity(self, item_id, action):
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=self.request.user)
        if action == 'increase':
            cart_item.quantity += 1
        elif action == 'decrease':
            cart_item.quantity -= 1
            if cart_item.quantity < 1:
                cart_item.delete()
                return JsonResponse({
                    'success': True,
                    'item_removed': True,
                    'cart_total_price': cart_item.cart.total_price
                })
        cart_item.save()

        return JsonResponse({
            'success': True,
            'new_quantity': cart_item.quantity,
            'item_total_price': cart_item.total_price,
            'cart_total_price': cart_item.cart.total_price
        })

    def clear_cart(self):
        cart = self.get_cart()
        if cart:
            cart.items.all().delete()
            return redirect('cart')
        return JsonResponse({'error': 'Cart not found'}, status=404)

    def remove_cart_item(self, item_id):
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=self.request.user)
        cart_item.delete()
        return redirect('cart')


# Views using the CartManager
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def add_to_cart(request):
    if request.method == "POST":
        body = json.loads(request.body)
        product_id = body.get('id')
        flavor_id = body.get('flavor')
        quantity = int(body.get('quantity', 1))
        manager = CartManager(request)
        return manager.add_to_cart(product_id, flavor_id, quantity)
    return JsonResponse({"error": "Invalid request method."}, status=400)

@csrf_exempt
def update_quantity(request):
    if request.method == "POST":
        body = json.loads(request.body)
        item_id = body.get('item_id')
        action = body.get('action')
        manager = CartManager(request)
        return manager.update_quantity(item_id, action)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@login_required
def clear_cart(request):
    manager = CartManager(request)
    return manager.clear_cart()

@login_required
def remove_cart_item(request, item_id):
    manager = CartManager(request)
    return manager.remove_cart_item(item_id)
