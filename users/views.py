from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Basket
from catalog_products.models import Products , ProductImage

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'{username} був успішно зараєстрований на сайті !')
            return redirect('/')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'users/profile.html')      # Декоратор який дає можливість відвідати дану сторінку тільки аутентифікованим користувачам

@login_required
def basket(request):
    basket_items = Basket.objects.filter(user=request.user)
    # Считаем общую сумму всех товаров в корзине
    total_basket_sum = sum(item.product.price * item.quantity for item in basket_items)

    return render(request, 'users/basket_profi.html', {
        'basket': basket_items,
        'total_sum': total_basket_sum})