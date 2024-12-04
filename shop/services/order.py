from django.db import transaction
from django.utils.timezone import localtime, now
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.contrib import messages
import json
from ..models import Cart, Order, OrderItem

import logging

logger = logging.getLogger(__name__)

class OrderService:
    def __init__(self, request):
        self.request = request

    def create_order(self):
        logger.info("Starting order creation process.")
        cart = self._get_user_cart()
        if not cart:
            messages.error(self.request, 'Your cart is empty!')
            logger.error("Cart is empty.")
            return None

        try:
            with transaction.atomic():
                logger.info("Transaction started.")
                order_data = self._extract_order_data(cart)
                logger.debug(f"Extracted order data: {order_data}")
                self._send_order_confirmation_email(order_data)
                logger.info("Order confirmation email sent.")
                order = self._create_order_record(order_data)
                logger.info(f"Order record created: {order}")
                self._create_order_items(cart, order)
                logger.info("Order items created successfully.")
                cart.delete()
                logger.info("Cart deleted after order placement.")
                messages.success(self.request, 'Order placed successfully!')
                return order
        except Exception as e:
            logger.error(f"Error placing order: {e}", exc_info=True)
            messages.error(self.request, f'Error placing order: {e}')
            return None

    def _get_user_cart(self):
        logger.info("Retrieving user's cart.")
        cart = Cart.objects.filter(user=self.request.user, is_active=True).first()
        if not cart:
            logger.warning("No active cart found for the user.")
        return cart

    def _extract_order_data(self, cart):
        try:
            logger.info("Extracting order data from the request and cart.")
            raw_body = self.request.body.decode('utf-8')
            logger.debug(f"Raw request body: {raw_body}")
            if not raw_body:
                raise ValueError("Request body is empty.")
            request_data = json.loads(raw_body)
            return {
                'customer_comment': request_data.get('comment', ''),
                'customer_phone': request_data.get('phone', ''),
                'shipping_address': request_data.get('shipping_address', ''),
                'shipping_type': request_data.get('shipping_type', 'STANDARD'),
                'coupon': request_data.get('coupon', ''),
                'cart_items': cart.items.all(),
                'cart': cart,
                'short_id': cart.short_id(),
                'order_time': localtime(now()),
                'domain': get_current_site(self.request).domain
            }
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in request body: {e}", exc_info=True)
            raise ValueError("Request body must contain valid JSON.")
        except Exception as e:
            logger.error(f"Error extracting order data: {e}", exc_info=True)
            raise

    def _send_order_confirmation_email(self, order_data):
        try:
            logger.info("Sending order confirmation email.")
            email_context = {
                'customer_comment': order_data['customer_comment'],
                'items': order_data['cart_items'],
                'cart': order_data['cart'],
                'short_id': order_data['short_id'],
                'order_time': order_data['order_time'],
                'domain': order_data['domain'],
                'phone': order_data['customer_phone']
            }
            email_html = render_to_string('shop/emails/order_email.html', email_context)
            text_content = strip_tags(email_html)
            subject = 'Your Order Details'
            to_email = order_data['cart'].user.email
            email = EmailMultiAlternatives(subject, text_content, to=[to_email])
            email.attach_alternative(email_html, "text/html")
            email.send()
            logger.info("Order confirmation email sent successfully.")
        except Exception as e:
            logger.error(f"Error sending order confirmation email: {e}", exc_info=True)
            raise

    def _create_order_record(self, order_data):
        try:
            logger.info("Creating order record.")
            return Order.objects.create(
                user=self.request.user,
                order_number=order_data['cart'].id,
                total_price=order_data['cart'].total_price,
                shipping_address=order_data['shipping_address'],
                shipping_type=order_data['shipping_type'],
                coupon=order_data['coupon'],
                status='NEW'
            )
        except Exception as e:
            logger.error(f"Error creating order record: {e}", exc_info=True)
            raise

    def _create_order_items(self, cart, order):
        try:
            logger.info("Creating order items from cart items.")
            for cart_item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    flavor=cart_item.flavor,  # Save the selected flavor
                    quantity=cart_item.quantity,
                    price=cart_item.total_price
                )
            logger.info("All order items created successfully.")
        except Exception as e:
            logger.error(f"Error creating order items: {e}", exc_info=True)
            raise

