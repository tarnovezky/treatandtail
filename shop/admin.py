from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from unfold.admin import ModelAdmin

from . import models
from .models import (
    UserAdditionalInfo,
    CallRequest,
    Subscription,
    Comment,
    Review,
    Product,
    ProductFlavor,
    Tag,
    Cart,
    CartItem,
    Order,
    OrderItem
)


# Inline for managing ProductFlavor within the Product admin
class ProductFlavorInline(admin.TabularInline):
    model = ProductFlavor
    extra = 1  # Number of empty rows to display for adding new flavors
    fields = ('flavor_name', 'price')  # Fields to display in the inline form


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ('name', 'name_eng',  'aviable_num', 'sale', 'expiration_months')
    search_fields = ('name', 'name_eng', 'article', 'brand_flavor')
    list_filter = ('sale', 'diet_type', 'age_range', 'item_form')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)
    inlines = [ProductFlavorInline]  # Attach ProductFlavor inline to Product


@admin.register(ProductFlavor)
class ProductFlavorAdmin(ModelAdmin):
    list_display = ('product', 'flavor_name', 'price')
    search_fields = ('product__name', 'flavor_name')
    list_filter = ('product',)


@admin.register(UserAdditionalInfo)
class UserAdditionalInfoAdmin(ModelAdmin):
    list_display = ('user', 'phone', 'date_of_birth', 'roles')
    search_fields = ('user__username', 'phone', 'roles')
    list_filter = ('roles',)
    fieldsets = (
        (None, {
            'fields': ('user', 'phone', 'date_of_birth', 'roles', 'picture'),
        }),
    )


@admin.register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(CallRequest)
class CallRequestAdmin(ModelAdmin):
    list_display = ('phone', 'status', 'order_time')
    list_filter = ('status', 'order_time')
    search_fields = ('phone',)
    ordering = ('-order_time',)


@admin.register(Comment)
class CommentAdmin(ModelAdmin):
    list_display = ('user', 'product', 'rating', 'time')
    list_filter = ('rating', 'time')
    search_fields = ('user__username', 'product__name', 'text')
    ordering = ('-time',)


@admin.register(Subscription)
class SubscriptionAdmin(ModelAdmin):
    list_display = ('user', 'email', 'subscribed', 'created_at', 'updated_at')
    list_filter = ('subscribed', 'created_at', 'updated_at')
    search_fields = ('user__username', 'email')


@admin.register(Cart)
class CartAdmin(ModelAdmin):
    list_display = [
        'short_cart_id_button',
        'user',
        'formatted_created_at',
        'status_with_background',
        'total_price',
        'view_cart_items'
    ]
    search_fields = ['id', 'user__username']
    list_filter = ['is_active', 'created_at']
    actions = ['mark_as_active', 'mark_as_inactive']

    def short_cart_id_button(self, obj):
        short_cart_id = str(obj.id)[:13]  # Get the first 13 characters of the Cart ID
        url = reverse('admin:shop_cart_change', args=[obj.id])  # Generate admin change URL
        return format_html(
            f'<a href="{url}" class="button" style="background-color: #8A8A8AFF; color: black; padding: 5px 10px; border-radius: 3px;">{short_cart_id}</a>'
        )
    short_cart_id_button.short_description = 'Cart ID'

    def formatted_created_at(self, obj):
        return obj.created_at.strftime('%d:%m:%y | %H:%M')
    formatted_created_at.short_description = 'Created At'

    def status_with_background(self, obj):
        color_map = {
            True: 'green',   # Active carts
            False: 'gray'    # Inactive carts
        }
        color = color_map.get(obj.is_active, 'black')
        status_display = 'Active' if obj.is_active else 'Inactive'
        return format_html(
            f'<span style="background-color: {color}; color: white; padding: 5px; border-radius: 3px;">{status_display}</span>'
        )
    status_with_background.short_description = 'Status'

    def view_cart_items(self, obj):
        url = reverse('admin:shop_cartitem_changelist') + f'?cart__id__exact={obj.id}'
        return format_html(
            f'<a href="{url}" class="button" style="background-color: #007BFF; color: white; padding: 5px 10px; border-radius: 3px;">View Items</a>'
        )
    view_cart_items.short_description = 'Cart Items'

    def mark_as_active(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "Selected carts have been marked as active.")
    mark_as_active.short_description = "Mark as Active"

    def mark_as_inactive(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "Selected carts have been marked as inactive.")
    mark_as_inactive.short_description = "Mark as Inactive"


@admin.register(CartItem)
class CartItemAdmin(ModelAdmin):
    list_display = ['product', 'quantity', 'cart', 'get_flavor']

    def get_flavor(self, obj):
        return obj.flavor.flavor_name if obj.flavor else "No Flavor"
    get_flavor.short_description = "Flavor"






@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = [
        'short_order_number_button',
        'user',
        'formatted_order_date',
        'status_with_background',
        'total_price',
        'view_order_items'
    ]
    search_fields = ['id', 'user__username', 'order_number']
    list_filter = ['status', 'order_date']
    actions = ['mark_as_completed', 'mark_as_canceled']

    def short_order_number_button(self, obj):
        short_order_number = obj.order_number[:13]  # Get the first 13 characters
        url = reverse('admin:shop_order_change', args=[obj.id])  # Generate admin change URL
        return format_html(
            f'<a href="{url}" class="button" style="background-color: #8A8A8AFF; color: black; padding: 5px 10px; border-radius: 3px;">{short_order_number}</a>'
        )
    short_order_number_button.short_description = 'Order Identifier'

    def formatted_order_date(self, obj):
        return obj.order_date.strftime('%d:%m:%y | %H:%M')
    formatted_order_date.short_description = 'Order Date'

    def status_with_background(self, obj):
        color_map = {
            'UNPAID': 'gray',
            'NEW': 'blue',
            'PROCESSING': 'orange',
            'COMPLETED': 'green',
            'CANCELED': 'red'
        }
        color = color_map.get(obj.status, 'black')
        return format_html(
            f'<span style="background-color: {color}; color: white; padding: 5px; border-radius: 3px;">{obj.get_status_display()}</span>'
        )
    status_with_background.short_description = 'Status'

    def view_order_items(self, obj):
        url = reverse('admin:shop_orderitem_changelist') + f'?order__id__exact={obj.id}'
        return format_html(
            f'<a href="{url}" class="button" style="background-color: #007BFF; color: white; padding: 5px 10px; border-radius: 3px;">View Items</a>'
        )
    view_order_items.short_description = 'Order Items'

    def mark_as_completed(self, request, queryset):
        queryset.update(status='COMPLETED')
        self.message_user(request, "Selected orders have been marked as completed.")
    mark_as_completed.short_description = "Mark as Completed"

    def mark_as_canceled(self, request, queryset):
        queryset.update(status='CANCELED')
        self.message_user(request, "Selected orders have been marked as canceled.")
    mark_as_canceled.short_description = "Mark as Canceled"




@admin.register(OrderItem)
class OrderItemAdmin(ModelAdmin):
    list_display = [

        'get_product_name',
        'get_flavor',
        'price',
        'quantity',
        'get_total_price',
        'get_username'
    ]
    search_fields = ['product__name', 'order__id']

    def get_product_name(self, obj):
        return obj.product.name
    get_product_name.short_description = "Product Name"

    def get_flavor(self, obj):
        return obj.flavor.flavor_name if obj.flavor else "No Flavor"
    get_flavor.short_description = "Flavor"

    def get_total_price(self, obj):
        return obj.total_price
    get_total_price.short_description = "Total Price"

    def get_username(self, obj):
        if obj.order.user:
            return obj.order.user.username
        return "Guest"

    get_username.short_description = "Username"


@admin.register(Review)
class ReviewAdmin(ModelAdmin):
    list_display = ("name", "rating", "created_by", "date_created", "last_edited")
    readonly_fields = ("created_by", "date_created", "last_edited")
    search_fields = ("name", "description")
    list_filter = ("rating", "date_created")

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # If creating a new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):
        return request.user.is_superuser
