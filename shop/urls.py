from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    ProductPageView, OurCompanyPageView, ContactUsPageView, ProductListView, CheckoutPageView,
    WhyUsPageView, CartPageView, ProductDetailView, AuthPageView, HomePageView)

from shop.controllers.auth import AuthController
from shop.controllers.cart import add_to_cart, update_quantity, clear_cart, remove_cart_item
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('cart/add/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', remove_cart_item, name='remove_cart_item'),
    path('cart/update_quantity/', update_quantity, name='update_quantity'),
    path('cart/clear/', clear_cart, name='clear_cart'),
    path('checkout/', CheckoutPageView.as_view(), name='checkout'),


    path('', HomePageView.as_view(), name='home'),

    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/<slug:slug>/<int:qty>/', ProductDetailView.as_view(), name='product_detail_qty'),

    path('our-company/', OurCompanyPageView.as_view(), name='our_company'),
    path('product/', ProductPageView.as_view(), name='product_page'),
    path('why-us/', WhyUsPageView.as_view(), name='why_us'),
    path('contact-us/', ContactUsPageView.as_view(), name='contact_us'),
    path('cart/', CartPageView.as_view(), name='cart'),



    path('auth/', AuthPageView.as_view(), name='auth'),
    path('signin', AuthController.signin, name='signin'),
    path('signup', AuthController.signup, name='signup'),
    path('activate/<uidb64>/<token>/', AuthController.activate, name='activate'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),



    path('reset_password/', auth_views.PasswordResetView.as_view(
        template_name="shop/auth/reset_password/password_reset.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
        template_name="shop/auth/reset_password/password_reset_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="shop/auth/reset_password/password_reset_form.html"), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name="shop/auth/reset_password/password_reset_done.html"), name="password_reset_complete")
]
