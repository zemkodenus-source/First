from django.urls import path
from . import views

urlpatterns = [
    path('', views.product, name='shop'),
    path('<int:pk>',views.product_detail , name = 'product_detail'),    # shop/1
]