from django.contrib.auth.models import User
from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save
from django.db import models
from users.models import CustomUser
from django.contrib.sessions.models import Session
from django.shortcuts import reverse


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name



class ProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    title = models.CharField(max_length=300)
    img = models.ImageField()
    price = models.DecimalField(max_digits=17, decimal_places=2)
    rating_num = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    is_active = models.BooleanField(default=True)
    objects = ProductManager()

    def __str__(self):
        return self.title





class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='product_img', on_delete=models.CASCADE)
    img = models.ImageField(upload_to='product_images')

    def __str__(self):
        return self.product.title


class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartItem')

    def __str__(self):
        return f"Cart for {self.user}"




class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=17, decimal_places=2, default=0)


    def __str__(self):
        return f"{self.product.title} - {self.quantity}"


class Rating(models.Model):
    SELECT = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5')
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=SELECT)

    def __str__(self):
        return f"{self.product.title} - {self.rating}"


@receiver(post_save, sender=Rating)
def update(sender, instance, created, **kwargs):
    product = Product.objects.get(pk=instance.product.id)
    ratings = Rating.objects.filter(product=product)
    rating_num = 0
    for rating in ratings:
        rating_num += rating.rating
    product.rating_num = rating_num / len(ratings)
    product.save()


class ContactMsg(models.Model):
    name = models.CharField(max_length=80)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    subject = models.CharField(max_length=160)
    message = models.TextField()
