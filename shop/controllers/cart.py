from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import get_object_or_404, redirect
from shop.models import Product, Cart, CartItem, ProductFlavor

@csrf_exempt
def add_to_cart(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return JsonResponse({"error": "User not authenticated"}, status=401)

        try:
            body = json.loads(request.body)
            product_id = body.get('id')  # Product ID
            flavor_id = body.get('flavor')  # Flavor ID
            quantity = int(body.get('quantity', 1))

            # Fetch the product and flavor
            product = get_object_or_404(Product, id=product_id)
            flavor = get_object_or_404(ProductFlavor, id=flavor_id) if flavor_id else None

            # Get or create the cart for the user
            cart, _ = Cart.objects.get_or_create(user=request.user, is_active=True)

            # Check if the item with the selected flavor already exists in the cart
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, flavor=flavor)

            if created:
                # If the item is new, set the quantity directly
                cart_item.quantity = quantity
            else:
                # If the item already exists, increment the quantity
                cart_item.quantity += quantity

            cart_item.save()

            return JsonResponse({
                "success": True,
                "message": f"{product.name} ({flavor.flavor_name if flavor else 'Default'}) added to cart.",
                "total_items": cart.items.count(),
                "cart_item_quantity": cart_item.quantity,
                "selected_flavor": flavor.flavor_name if flavor else "No Flavor"
            })

        except Product.DoesNotExist:
            return JsonResponse({"error": "Product does not exist."}, status=404)
        except ProductFlavor.DoesNotExist:
            return JsonResponse({"error": "Flavor does not exist."}, status=404)
        except ValueError:
            return JsonResponse({"error": "Invalid quantity."}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=400)



def update_quantity(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        item_id = data.get('item_id')
        action = data.get('action')

        try:
            cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

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

        except CartItem.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Cart item not found'})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})





@login_required
def clear_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user, is_active=True).first()
    if cart:
        cart.items.all().delete()
    return redirect('cart')

def remove_cart_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect('cart')
