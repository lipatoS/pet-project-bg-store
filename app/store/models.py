from django.db import models


# Create your models here.


class Category(models.Model):
    category_name = models.CharField(max_length=255)


class GameCategory(models.Model):
    game_category_name = models.CharField(max_length=255)


class Product(models.Model):
    name = models.CharField(max_length=255)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField()
    game_category = models.ForeignKey(GameCategory, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='products/images/', null=True, blank=True)