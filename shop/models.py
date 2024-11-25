from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
from django.urls import reverse
import uuid

User = get_user_model()


class UserAdditionalInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='additional_info', verbose_name=_("User"))
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name=_("Phone Number"))
    picture = models.ImageField(upload_to='user_pictures/', blank=True, null=True, verbose_name=_("Profile Picture"))
    date_of_birth = models.DateField(blank=True, null=True, verbose_name=_("Date of Birth"))
    roles = models.CharField(
        max_length=50,
        choices=[('admin', _('Admin')), ('customer', _('Customer')), ('other', _('Other'))],
        default='customer',
        verbose_name=_("Role")
    )

    class Meta:
        verbose_name = _("User Additional Info")
        verbose_name_plural = _("Users Additional Info")

    def __str__(self):
        return f"{self.user.username}'s Additional Info"


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Tag Name")

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Product Name")
    name_eng = models.CharField(max_length=255, verbose_name="Product Name (English)", blank=True, null=True)
    description = models.TextField(verbose_name="Description", blank=True, null=True)
    ingredients = models.TextField(verbose_name="Ingredients", blank=True, null=True)
    slug = models.SlugField(unique=True)
    article = models.CharField(max_length=50, verbose_name="Article")
    image = models.ImageField(upload_to="products/", verbose_name="Product Image", blank=True, null=True)
    aviable_num = models.IntegerField(verbose_name="Available Quantity", default=0)
    weight = models.FloatField(verbose_name="Weight (kg)", blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")
    sale = models.IntegerField(verbose_name="Discount Percentage", blank=True, null=True)
    brand_flavor = models.CharField(max_length=100, verbose_name="Brand/Flavor", blank=True, null=True)
    diet_type = models.CharField(max_length=100, verbose_name="Diet Type", blank=True, null=True)
    age_range = models.CharField(max_length=100, verbose_name="Age Range", blank=True, null=True)
    item_form = models.CharField(max_length=50, verbose_name="Item Form", blank=True, null=True)
    width = models.FloatField(verbose_name="Width (cm)", blank=True, null=True)
    height = models.FloatField(verbose_name="Height (cm)", blank=True, null=True)
    expiration_months = models.IntegerField(verbose_name="Months to Expiration", blank=True, null=True)
    tags = models.ManyToManyField("Tag", verbose_name="Tags", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def get_absolute_url(self):
        return reverse('buy_now', kwargs={'slug': self.slug})


    def __str__(self):
        return self.name


class ProductFlavor(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="flavors", verbose_name="Product")
    flavor_name = models.CharField(max_length=100, verbose_name="Flavor Name")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Flavor Price")

    class Meta:
        verbose_name = "Product Flavor"
        verbose_name_plural = "Product Flavors"

    def __str__(self):
        return f"{self.flavor_name} - {self.product.name}"


class CallRequest(models.Model):
    STATUS_CHOICES = [
        ('NEW', 'New'),
        ('VIEWED', 'Viewed'),
        ('DONE', 'Done'),
    ]

    phone = models.CharField(max_length=20, verbose_name="Phone Number")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='NEW', verbose_name="Status")
    order_time = models.DateTimeField(default=now, verbose_name="Order Time")

    class Meta:
        verbose_name = "Call Request"
        verbose_name_plural = "Call Requests"

    def __str__(self):
        return f"{self.phone} - {self.get_status_display()}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User", related_name="comments")
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name="Product", related_name="comments")
    time = models.DateTimeField(default=now, verbose_name="Time of Comment")
    text = models.TextField(verbose_name="Comment Text")
    rating = models.PositiveSmallIntegerField(default=5, verbose_name="Rating (1-5)")

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ['-time']

    def __str__(self):
        return f"Comment by {self.user.username} on {self.product.name}"


class Review(models.Model):
    name = models.CharField(max_length=255, verbose_name="Review Name")
    images = models.ImageField(upload_to="reviews/images/", blank=True, null=True, verbose_name="Review Images")
    description = models.TextField(verbose_name="Description")
    rating = models.DecimalField(max_digits=3, decimal_places=1, verbose_name="Rating (0-5)")
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="created_reviews",
        editable=False,
        verbose_name="Created by"
    )
    date_created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="Date Created")
    last_edited = models.DateTimeField(auto_now=True, verbose_name="Last Edited")

    def save(self, *args, **kwargs):
        if not self.pk and not self.created_by:
            raise ValueError("The 'created_by' field must be set when creating a review.")
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"

    def __str__(self):
        return f"{self.name} (Rating: {self.rating})"


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="subscriptions")
    email = models.EmailField(verbose_name="Subscription Email")
    subscribed = models.BooleanField(default=True, verbose_name="Is Subscribed")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Subscribed On")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last Updated")
    topics = models.JSONField(default=dict, blank=True, verbose_name="Topics Preferences")

    class Meta:
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"
        unique_together = ('user', 'email')

    def __str__(self):
        return f"{self.user.username} ({self.email}) - {'Subscribed' if self.subscribed else 'Unsubscribed'}"




class Cart(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, max_length=10)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carts", verbose_name="User")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last Updated")
    is_active = models.BooleanField(default=True, verbose_name="Active")

    @property
    def num_of_items(self):
        cartitems = self.cartitems.all()
        quantity = sum([item.quantity for item in cartitems])
        return quantity
    def short_id(self):
        return f" {str(self.id)[:13]}"


    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Carts"

    def __str__(self):
        return f"Cart ({self.id}) for {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items", verbose_name="Cart")
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name="cart_items", verbose_name="Product")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Quantity")

    class Meta:
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Cart ({self.cart.id})"

    @property
    def total_price(self):
        return self.product.price * self.quantity




class Order(models.Model):
    STATUS_CHOICES = [
        ('NEW', 'New'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('CANCELED', 'Canceled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders", verbose_name="User")
    order_number = models.CharField(max_length=36, unique=True, verbose_name="Order Identifier")
    order_date = models.DateTimeField(auto_now_add=True, verbose_name="Order Date")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEW', verbose_name="Order Status")
    total_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Total Price")

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return f"Order ({self.order_number}) for {self.user.username} - {self.status}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items", verbose_name="Order")
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name="order_items", verbose_name="Product")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Quantity")
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Unit Price")

    class Meta:
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order ({self.order.id})"

    @property
    def total_price(self):
        return self.price * self.quantity
