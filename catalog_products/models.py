# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User  # ← імпорт вбудованої моделі User для створення Comments + User + Product

# Функція для динамічного шляху: media/products/product_ID/filename
def product_directory_path(instance, filename):
    # Якщо це головне фото (модель Products)
    if hasattr(instance, 'id') and instance.id:
        return f'products/product_{instance.id}/{filename}'
    # Якщо це додаткове фото (модель ProductImage)
    return f'products/product_{instance.product.id}/{filename}'


class Products(models.Model):
        # Django автоматично бачить 'id' як Primary Key, але можна прописати явно
    id = models.AutoField(primary_key=True)
    product = models.CharField(max_length=50, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)  # Великий текст
        # Для PostgreSQL JSONField — найкращий варіант для характеристик
    specifications = models.JSONField(blank=True, null=True)
        # ГОЛОВНЕ ФОТО
    main_image = models.ImageField(upload_to=product_directory_path, blank=True, null=True)
        # нові категорії для функції фільтрації
    brand = models.CharField(max_length=50, blank=True, null=True)
    category = models.CharField(max_length=50, blank=True, null=True)
    ram_gb = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'products'

    def __str__(self):
        return self.product


# МОДЕЛЬ ДЛЯ ГАЛЕРЕЇ (багато фото до одного товару)
class ProductImage(models.Model):
    product = models.ForeignKey(Products, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=product_directory_path)

    class Meta:
        managed = True
        db_table = 'product_images'

class Comments(models.Model):
    product = models.ForeignKey(
        Products,                       #   прив'язуємо до моделі Products
        on_delete=models.CASCADE,       #   якщо товар видалено — коментарі теж видаляються
        related_name='comments',        #   щоб звертатись: product.comments.all()
    )
    user = models.ForeignKey(
        User,                           # Прив'язуємо до User
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} → {self.product}'        # При зверненні до коментаря нам відразу підтягує User та Product