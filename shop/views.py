from shop.models import Review
from django.views.generic import ListView
from django.views.generic import DetailView
from .models import Product
from django.views.generic import TemplateView, View
from .models import Cart, CartItem
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import json
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.http import JsonResponse
from shop.services.order import OrderService

class ProductPageView(TemplateView):
    template_name = 'shop/pages/product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class ProductListView(ListView):
    model = Product
    template_name = 'shop/pages/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['product_name'] = "Sample Product"
        context['product_price'] = 100

        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/pages/buy.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object

        # Get quantity from the URL parameter, defaulting to 1
        qty = self.kwargs.get('qty', 1)
        try:
            quantity = int(qty)
            if quantity < 1:
                quantity = 1  # Ensure quantity is at least 1
        except ValueError:
            quantity = 1  # Fallback if qty is not an integer

        context['quantity'] = quantity

        # Calculate the rating as a percentage (rating out of 5 stars)
        rating_percentage = (product.rating / 5) * 100 if product.rating else 0
        context['rating_percentage'] = rating_percentage

        # Fetch related flavors or provide a default message
        context['flavors'] = product.flavors.all()

        # Add stock availability info
        context['in_stock'] = product.aviable_num > 0

        return context




class OurCompanyPageView(TemplateView):
    template_name = 'shop/pages/company.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['product_name'] = "Sample Product"
        context['product_price'] = 100

        return context

class HomePageView(TemplateView):
    template_name = 'shop/pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['product_name'] = "Sample Product"
        context['product_price'] = 100

        return context

class AuthPageView(TemplateView):
    template_name = 'shop/pages/auth.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['product_name'] = "Sample Product"
        context['product_price'] = 100

        return context



class ContactUsPageView(TemplateView):
    template_name = 'shop/pages/contact_us.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['product_name'] = "Sample Product"
        context['product_price'] = 100


        return context










class CartPageView(TemplateView):
    template_name = 'shop/pages/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        session_key = self.request.session.session_key

        if user.is_authenticated:
            cart = Cart.objects.filter(user=user, is_active=True).first()
        else:
            cart = Cart.objects.filter(session_key=session_key, is_active=True).first()

        context['cart'] = cart
        return context






class RemoveCartItemView(View):
    def post(self, request, item_id):
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'error': 'Unauthorized'}, status=403)

        # Find the cart item and delete it
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=user)
        cart_item.delete()

        return redirect('cart_page')  # Redirect to the cart page



class WhyUsPageView(TemplateView):
    template_name = 'shop/pages/why_us.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reviews = Review.objects.all()[:12]
        for review in reviews:
            review.rating_percentage = (review.rating / 5) * 100
        context['reviews'] = reviews
        return context









from django.views.generic import TemplateView
from django.http import JsonResponse
from .services.order import OrderService

import logging

logger = logging.getLogger(__name__)

class CheckoutPageView(TemplateView):
    template_name = 'shop/pages/checkout.html'

    def get_context_data(self, **kwargs):
        logger.info("Rendering checkout page.")
        context = super().get_context_data(**kwargs)
        context['shipping_options'] = [
            {'value': 'STANDARD', 'label': 'Standard'},
            {'value': 'EXPRESS', 'label': 'Express'},
            {'value': 'PICKUP', 'label': 'On-hand in Shop'},
        ]
        logger.debug(f"Checkout page context: {context}")
        return context

    def post(self, request, *args, **kwargs):
        logger.info("Received POST request for checkout.")
        try:
            order_service = OrderService(request)
            order = order_service.create_order()
            if order:
                logger.info(f"Order created successfully: {order.order_number}")
                return JsonResponse({'status': 'success', 'order_number': order.order_number})
            logger.warning("Order creation failed.")
            return JsonResponse({'status': 'error', 'message': 'Failed to place order.'})
        except Exception as e:
            logger.error(f"Error during checkout: {e}", exc_info=True)
            return JsonResponse({'status': 'error', 'message': str(e)})






from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from shop.controllers.cart import CartManager

@receiver(user_logged_in)
def merge_carts_on_login(sender, request, user, **kwargs):
    """
    Merge the session cart into the user's cart after login.
    """
    manager = CartManager(request)
    manager.merge_carts()

