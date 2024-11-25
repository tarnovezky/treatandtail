from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import get_object_or_404
from shop.models import Product, Cart, CartItem


@csrf_exempt
def add_to_cart(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return JsonResponse({"error": "User not authenticated"}, status=401)

        try:
            body = json.loads(request.body)
            product_id = body.get('id')  # Use 'id' matching the button value
            flavor = body.get('flavor')  # Get selected flavor
            quantity = int(body.get('quantity', 1))

            # Fetch the product using id
            product = get_object_or_404(Product, id=product_id)

            # Get or create the cart for the user
            cart, _ = Cart.objects.get_or_create(user=request.user, is_active=True)

            # Check if the item already exists in the cart
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            cart_item.quantity += quantity
            cart_item.flavor = flavor  # Save the selected flavor
            cart_item.save()

            return JsonResponse({
                "success": True,
                "message": f"{product.name} ({flavor}) added to cart.",
                "total_items": cart.items.count(),  # Use the related_name 'items' here
                "cart_item_quantity": cart_item.quantity,
                "selected_flavor": flavor
            })

        except Product.DoesNotExist:
            return JsonResponse({"error": "Product does not exist."}, status=404)
        except ValueError:
            return JsonResponse({"error": "Invalid quantity."}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=400)
