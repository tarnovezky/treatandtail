from django.contrib import admin  # Ensure this is imported
from django.urls import reverse
from django.utils.html import format_html
from unfold.admin import ModelAdmin  # Import Unfold's ModelAdmin

from .models import (
    UserAdditionalInfo,
    CallRequest, Subscription,
    Comment, Review,
    Product, Tag,
    Cart, CartItem, Order, OrderItem
)

admin.site.site_header = "TreatAndTail Administration"  # Optional: Admin panel header
admin.site.site_title = "TreatAndTail Admin"            # Title shown in the browser tab
admin.site.index_title = "Welcome to TreatAndTail Admin"  # Optional: Title for the index page


@admin.register(UserAdditionalInfo)
class UserAdditionalInfoAdmin(ModelAdmin):  # Use Unfold's ModelAdmin
    list_display = ('user', 'phone', 'date_of_birth', 'roles')
    search_fields = ('user__username', 'phone', 'roles')
    list_filter = ('roles',)
    fieldsets = (
        (None, {
            'fields': ('user', 'phone', 'date_of_birth', 'roles', 'picture'),
        }),
    )


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ('name', 'name_eng', 'price', 'aviable_num', 'sale', 'expiration_months')
    search_fields = ('name', 'name_eng', 'article', 'brand_flavor')
    list_filter = ('sale', 'diet_type', 'age_range', 'item_form')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)


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
    list_display = ['user', 'get_cart_id', 'total_price', 'view_cart_items']
    search_fields = ['id', 'user__username']
    list_filter = ['is_active', 'created_at']

    def get_cart_id(self, obj):
        url = reverse('admin:shop_cart_change', args=[obj.id])
        return format_html(f'<a href="{url}" class="button">{str(obj.id)[:13]}</a>')

    get_cart_id.short_description = 'Cart ID'

    def view_cart_items(self, obj):
        url = reverse('admin:shop_cartitem_changelist')
        return format_html(f'<a href="{url}?cart__id__exact={obj.id}" class="button">View</a>')

    view_cart_items.short_description = 'Cart Items'


@admin.register(CartItem)
class CartItemAdmin(ModelAdmin):
    list_display = ['product', 'quantity', 'cart']


@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = ['id', 'user', 'get_order_number_button', 'order_date', 'status', 'view_order_items']
    search_fields = ['id', 'user__username', 'order_number']
    list_filter = ['status', 'order_date']

    def get_order_number_button(self, obj):
        url = reverse('admin:shop_order_change', args=[obj.id])
        return format_html(f'<a href="{url}" class="button">{obj.order_number[:13]}</a>')

    get_order_number_button.short_description = 'Order Identifier'

    def view_order_items(self, obj):
        url = reverse('admin:shop_orderitem_changelist')
        return format_html(f'<a href="{url}?order__id__exact={obj.id}" class="button">View</a>')

    view_order_items.short_description = 'Order Items'

    actions = ['mark_as_completed', 'mark_as_canceled']

    def mark_as_completed(self, request, queryset):
        queryset.update(status='COMPLETED')
        self.message_user(request, "Selected orders have been marked as completed.")

    def mark_as_canceled(self, request, queryset):
        queryset.update(status='CANCELED')
        self.message_user(request, "Selected orders have been marked as canceled.")

    mark_as_completed.short_description = "Mark as Completed"
    mark_as_canceled.short_description = "Mark as Canceled"


@admin.register(OrderItem)
class OrderItemAdmin(ModelAdmin):
    list_display = ['product', 'quantity', 'price', 'order']
    search_fields = ['product__name', 'order__id']


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
