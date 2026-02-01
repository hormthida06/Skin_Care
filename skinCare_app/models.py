
from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from decimal import Decimal
# =========================================== Product ====================================
class Product(models.Model):

    SKIN_TYPE_CHOICES = [
        ('All', 'All'),
        ('Dry', 'Dry'),
        ('Oily', 'Oily'),
        ('Sensitive', 'Sensitive'),
        ('Combination', 'Combination'),
    ]

    product_id = models.AutoField(primary_key=True)

    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='category_id'
    )

    concerns = models.ManyToManyField(
        'Concern',
        through='ProductConcern',
        related_name='products',
        blank=True
    )

    product_name = models.CharField(max_length=255, null=True, blank=True)
    brand = models.CharField(max_length=255, null=True, blank=True)
    skin_type = models.CharField(max_length=20, choices=SKIN_TYPE_CHOICES, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    ingredients = models.TextField(null=True, blank=True)
    using = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.IntegerField(null=True, blank=True)
    image_url = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'products'

    def __str__(self):
        return self.product_name or "Unnamed Product"

# =========================================== Category ====================================
class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'categories'
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.category_name or "Unnamed Category"

# =========================================== Concern ====================================
class Concern(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'concerns'
        verbose_name_plural = "Concerns"

    def __str__(self):
        return self.name or "Unnamed Concern"

# =========================================== Product Concern ====================================
class ProductConcern(models.Model):
    id = models.BigAutoField(primary_key=True)

    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        db_column='product_id'
    )

    concern = models.ForeignKey(
        'Concern',
        on_delete=models.CASCADE,
        db_column='concern_id'
    )

    class Meta:
        db_table = 'products_concerns'
        unique_together = ('product', 'concern')

    def __str__(self):
        return f"{self.product_id} - {self.concern_id}"

# =========================================== User ====================================
class User(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('customer', 'Customer'),
    ]

    user_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')
    created_at = models.DateTimeField()

    class Meta:
        db_table = 'users'
        managed = False

    def set_password(self, raw_password):
        from django.contrib.auth.hashers import make_password
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        from django.contrib.auth.hashers import check_password
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.user_name

# =========================================== Profile ====================================
class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('F', 'Female'),
        ('M', 'Male'),
    ]

    id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    user = models.OneToOneField(
        'User',
        on_delete=models.CASCADE,
        unique=True,
        db_column='user_id'
    )

    class Meta:
        db_table = 'user_profiles'
        managed = False

    def __str__(self):
        return self.full_name or f"Profile {self.id}"

# =========================================== Order ====================================
class Order(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, null=True, blank=True)
    delivery_status = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'orders'
        managed = False
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.order_id} - {self.user}"

# =========================================== Order Item ====================================
class OrderItem(models.Model):
    order_item_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        db_table = 'order_items'
        managed = False

    def __str__(self):
        return f"{self.product} x {self.quantity} (Order #{self.order.order_id})"

    def save(self, *args, **kwargs):
        # Automatically calculate subtotal if not provided
        if self.product and not self.subtotal:
            self.subtotal = self.product.price * self.quantity
        super().save(*args, **kwargs)

# =========================================== Cart ====================================

class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        null=True,
        db_column='user_id'
    )
    created_at = models.DateTimeField(null=True)

    class Meta:
        db_table = 'cart'
        managed = False

    def __str__(self):
        return f"Cart {self.cart_id} for User {self.user_id}"

# =========================================== Cart Item ====================================
class CartItem(models.Model):
    id = models.AutoField(primary_key=True)
    cart = models.ForeignKey(
        'Cart',
        on_delete=models.CASCADE,
        db_column='cart_id'
    )
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        db_column='product_id'
    )
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = 'cart_item'
        managed = False  # If you want Django to not touch the DB table

    def __str__(self):
        return f"{self.quantity} x {self.product} in Cart {self.cart_id}"

    @property
    def subtotal(self):
        if self.product and self.product.price:
            return self.quantity * self.product.price
        return Decimal('0.00')

# =========================================== Payment ====================================
class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('Card', 'Card'),
        ('PayPal', 'PayPal'),
        ('KHQR', 'KHQR'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Success', 'Success'),
        ('Failed', 'Failed'),
    ]

    payment_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(
        'Order',
        on_delete=models.CASCADE,
        null=True,
        db_column='order_id'
    )
    payment_method = models.CharField(
        max_length=10,
        choices=PAYMENT_METHOD_CHOICES,
        null=True,
        default='KHQR'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        null=True
    )
    transaction_id = models.CharField(max_length=255, null=True)
    paid_at = models.DateTimeField(null=True)

    class Meta:
        db_table = 'payments'

    def __str__(self):
        return f"Payment {self.payment_id} - {self.status}"
