from django.contrib import admin
from .models import Products, ProductImage , Comments
from users.models import Basket
# Register your models here.

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3 # Кількість порожніх слотів для фото

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]


# Застарілий спосіб реєстрації та робочий
# admin.site.register(Comments)


# Професійний підхід
@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'created_at']  # колонки в списку
    list_filter = ['created_at']                         # фільтр справа
    search_fields = ['author__username', 'text']         # пошук


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ['user' , 'product']
    search_fields = ['user__username']