from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from shop.models import Cart, CartItem


@receiver(user_logged_in)
def merge_guest_cart(sender, request, user, **kwargs):
    """Merge guest cart with authenticated cart upon login."""
    session_key = request.session.session_key
    if not session_key:
        return  # No session, nothing to merge

    guest_cart = Cart.objects.filter(session_key=session_key, is_active=True).first()

    if guest_cart:
        # Get or create the authenticated user's cart
        auth_cart, _ = Cart.objects.get_or_create(user=user, is_active=True)

        # Merge items from the guest cart into the authenticated cart
        for item in guest_cart.items.all():
            auth_item, created = CartItem.objects.get_or_create(
                cart=auth_cart,
                product=item.product,
                flavor=item.flavor
            )
            if not created:
                auth_item.quantity += item.quantity
                auth_item.save()
            item.delete()

        # Deactivate the guest cart
        guest_cart.is_active = False
        guest_cart.save()


@receiver(user_logged_out)
def clear_cart_session(sender, request, user, **kwargs):
    """Clear guest cart session after logout."""
    session_key = request.session.session_key
    if session_key:
        Cart.objects.filter(session_key=session_key, is_active=True).delete()
