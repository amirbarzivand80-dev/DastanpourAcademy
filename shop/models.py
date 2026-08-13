from django.db import models


class Category(models.Model):

    name = models.CharField(max_length=100)

    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Brand(models.Model):

    name = models.CharField(max_length=100)

    slug = models.SlugField(unique=True)

    logo = models.ImageField(
        upload_to="brands/",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name


class Product(models.Model):

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products"
    )

    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products"
    )

    name = models.CharField(max_length=200)

    slug = models.SlugField(unique=True)

    description = models.TextField()

    price = models.PositiveIntegerField()

    discount_price = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    stock = models.PositiveIntegerField(default=0)

    image = models.ImageField(
        upload_to="products/"
    )

    is_active = models.BooleanField(default=True)
    
    show_on_home = models.BooleanField(default=False)
    
    related_products = models.ManyToManyField(
        "self",
        blank=True,
        symmetrical=False,
        related_name="recommended_for"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ProductImage(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="gallery"
    )

    image = models.ImageField(
        upload_to="product_gallery/"
    )

class ProductSpecification(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="specifications"
    )

    title = models.CharField(max_length=150)

    value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.product.name} - {self.title}"


class ProductFeature(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="features"
    )

    title = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.product.name} - {self.title}"
    
class Cart(models.Model):

    user = models.OneToOneField(
    "users.CustomUser",
    on_delete=models.CASCADE
)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Cart - {self.user}"


class CartItem(models.Model):

    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    def total_price(self):

        if self.product.discount_price:
            price = self.product.discount_price
        else:
            price = self.product.price

        return price * self.quantity


    def __str__(self):
        return self.product.name
    
class Order(models.Model):

    STATUS_CHOICES = (
        ("pending", "در انتظار پرداخت"),
        ("paid", "پرداخت شده"),
        ("sent", "ارسال شده"),
        ("completed", "تکمیل شده"),
        ("cancelled", "لغو شده"),
    )

    DELIVERY_CHOICES = (
        ("self", "خودم تحویل می‌گیرم"),
        ("other", "شخص دیگر تحویل می‌گیرد"),
    )

    user = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.CASCADE,
        related_name="orders"
    )

    # -----------------------------
    # اطلاعات خریدار
    # -----------------------------

    full_name = models.CharField(
        max_length=100
    )

    phone = models.CharField(
        max_length=11
    )

    postal_code = models.CharField(
        max_length=10
    )

    address = models.TextField()

    # -----------------------------
    # اطلاعات تحویل گیرنده
    # -----------------------------

    delivery_type = models.CharField(
        max_length=10,
        choices=DELIVERY_CHOICES,
        default="self"
    )

    receiver_name = models.CharField(
        max_length=100,
        blank=True
    )

    receiver_phone = models.CharField(
        max_length=11,
        blank=True
    )

    # -----------------------------
    # مبلغ سفارش
    # -----------------------------

    total_price = models.PositiveIntegerField(
        default=0
    )

    # -----------------------------
    # وضعیت سفارش
    # -----------------------------

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"Order {self.id} - {self.user}"
class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )


    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )


    quantity = models.PositiveIntegerField(
        default=1
    )


    price = models.PositiveIntegerField()


    def total_price(self):

        return self.price * self.quantity
    
from django.conf import settings


class Favorite(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="favorites"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="favorite_products"
    )

    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        unique_together = ("user", "product")


    def __str__(self):
        return f"{self.user.full_name} - {self.product.name}"
    

class ProductComment(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="product_comments"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    text = models.TextField()


    rating = models.PositiveIntegerField(
        default=5
    )


    is_active = models.BooleanField(
        default=False
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):

        return f"{self.user.full_name} - {self.product.name}"