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

    def create_order(self, data):
        logger.info("Starting order creation process.")
        cart = self._get_user_cart()
        if not cart:
            messages.error(self.request, 'Your cart is empty!')
            logger.error("Cart is empty.")
            return None

        try:
            with transaction.atomic():
                logger.info("Transaction started.")
                order_data = self._extract_order_data(cart, data)
                logger.debug(f"Extracted order data: {order_data}")
                order = self._create_order_record(order_data)
                logger.info(f"Order record created: {order}")
                self._create_order_items(cart, order)
                logger.info("Order items created successfully.")
                if self.request.user.is_authenticated:
                    self._send_order_confirmation_email(order_data)
                    logger.info("Order confirmation email sent.")
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
        if self.request.user.is_authenticated:
            cart = Cart.objects.filter(user=self.request.user, is_active=True).first()
        else:
            session_key = self.request.session.session_key
            if not session_key:
                self.request.session.create()
                session_key = self.request.session.session_key
            cart = Cart.objects.filter(session_key=session_key, is_active=True).first()

        if not cart:
            logger.warning("No active cart found.")
        return cart

    def _extract_order_data(self, cart, data):
        try:
            logger.info("Extracting order data from the request and cart.")
            return {
                'name': data.get('name', '') if not self.request.user.is_authenticated else self.request.user.get_full_name(),
                'email': data.get('email', '') if not self.request.user.is_authenticated else self.request.user.email,
                'customer_comment': data.get('comment', ''),
                'customer_phone': data.get('phone', ''),
                'shipping_address': data.get('shipping_address', ''),
                'shipping_type': data.get('shipping_type', 'STANDARD'),
                'coupon': data.get('coupon', ''),
                'cart_items': cart.items.all(),
                'cart': cart,
                'short_id': cart.short_id(),
                'order_time': localtime(now()),
                'domain': get_current_site(self.request).domain
            }
        except Exception as e:
            logger.error(f"Error extracting order data: {e}", exc_info=True)
            raise ValueError("Invalid request data.")

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
            to_email = order_data['email']
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
                user=self.request.user if self.request.user.is_authenticated else None,
                name=order_data['name'],
                email=order_data['email'],
                order_number=order_data['cart'].id,
                total_price=order_data['cart'].total_price,
                shipping_address=order_data['shipping_address'],
                shipping_type=order_data['shipping_type'],
                coupon=order_data['coupon'],
                status='UNPAID'
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
                    flavor=cart_item.flavor,
                    quantity=cart_item.quantity,
                    price=cart_item.total_price
                )
            logger.info("All order items created successfully.")
        except Exception as e:
            logger.error(f"Error creating order items: {e}", exc_info=True)
            raise
