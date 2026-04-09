from django.shortcuts import render, get_object_or_404, redirect
from .models import Products , Comments
from .forms import CommentsForm

#def products(request):                           # URL  'SHOP'
#    products = Products.objects.all()                                                      # даний def вже не використовується оскільки появився новий
#    return render(request, 'catalog_products/shop.html', {'products': products})           # покращений із можливість фільтрації


# частина СОРТУВАННЯ товарів користувачем
def product(request):
    # Отримуємо ВСІ товари з бази даних
                                                            #   ДОДАТКОВО    Product.objects.all() повертає QuerySet — набір всіх товарів
    products = Products.objects.all()

    # -------------------------------------------------------
    # Зчитуємо параметри фільтрації з URL (GET-запит)
    # Наприклад: /shop/?category=phone&price_min=100
    # Якщо параметр відсутній в URL — повертає None
    # -------------------------------------------------------
    category = request.GET.get('category')          # наприклад: "phone"
    brand = request.GET.get('brand')                # наприклад: "Samsung"
    price_min = request.GET.get('price_min')        # наприклад: "100"
    price_max = request.GET.get('price_max')        # наприклад: "2000"
    search = request.GET.get('search')              # наприклад: "Galaxy"
    ram_gb = request.GET.get('ram_gb')              # наприклад: "12 gb"
    if ram_gb:
        ram_gb = int(ram_gb)

    # -------------------------------------------------------
    # Застосовуємо фільтри — тільки якщо параметр передано
    # Кожен .filter() звужує QuerySet і повертає новий QuerySet
    # -------------------------------------------------------

    # Фільтр по категорії (точний збіг)
    if category:
        products = products.filter(category=category)

    # Фільтр по бренду (без урахування регістру, часткове співпадіння)
    # icontains = case-insensitive contains ("samsung" знайде "Samsung")
    if brand:
        products = products.filter(brand__icontains=brand)

    # Фільтр по мінімальній ціні
    # gte = greater than or equal (більше або рівно)
    if price_min:
        products = products.filter(price__gte=price_min)

    # Фільтр по максимальній ціні
    # lte = less than or equal (менше або рівно)
    if price_max:
        products = products.filter(price__lte=price_max)

    # Пошук по назві товару (без урахування регістру)
    if search:
        products = products.filter(product__icontains=search)

    # Пошук по RAM
    if ram_gb:
        products = products.filter(ram_gb=ram_gb)

    # -------------------------------------------------------
    # Отримуємо унікальні значення для випадаючих списків у формі
    # distinct() прибирає дублікати
    # -------------------------------------------------------

    # Product.objects  # звертаємось до таблиці Product
    # .values_list('....', flat=True)  # беремо ТІЛЬКИ колонку "..ram..." → [8, 8, 12, 16, 8]
    # .distinct()  # прибираємо дублікати → [8, 12, 16]
    #-------------------------------------------------------------------------------------------------------
                                            # Product.objects
                                            # # Звертаємось до таблиці Product
                                            # # Результат: всі 5 рядків таблиці
                                            #
                                            # .values_list('category', flat=True)
                                            # # Беремо ТІЛЬКИ колонку 'category'
                                            # # Результат: ['Телефон', 'Телефон', 'Телевізор', 'Аксесуар', 'Телефон']
                                            #
                                            # .distinct()
                                            # Прибираємо дублікати
                                            # Результат: ['Телефон', 'Телевізор', 'Аксесуар']
    #-------------------------------------------------------------------------------------------------------


    categories = Products.objects.values_list('category', flat=True).distinct()
    brands = Products.objects.values_list('brand', flat=True).distinct()

    ram_gb_options = Products.objects.values_list('ram_gb', flat=True).exclude(ram_gb__isnull=True).distinct()
    ram_gb_options = sorted(ram_gb_options)  # сортування за зростанням

    # -------------------------------------------------------
    # Передаємо дані в HTML шаблон через словник context
    # У шаблоні звертаємось до них як {{ products }}, {{ categories }} і т.д.
    # -------------------------------------------------------
    context = {
        'products': products,  # відфільтровані товари
        'categories': categories,  # список категорій для <select>
        'brands': brands,  # список брендів для <select>
        'selected_category': category,  # щоб показати обраний фільтр               # ця змінна передані в html для збереженя результатів фільтрації
        'selected_brand': brand,  # щоб показати обраний фільтр                     # ця змінна передані в html для збереженя результатів фільтрації
        'price_min': price_min,  # щоб зберегти значення в полі
        'price_max': price_max,  # щоб зберегти значення в полі
        'search': search,  # щоб зберегти текст пошуку
        'ram_gb': ram_gb_options ,
        'selected_ram_gb': ram_gb                                                   # ця змінна передані в html для збереженя результатів фільтрації
    }

    # Рендеримо шаблон і повертаємо HTML сторінку користувачу
    return render(request, 'catalog_products/shop.html', context)


def product_detail(request, pk):                               # сторінка ДЕТАЛЬНІШЕ для кожного іх товарів
    product = get_object_or_404(Products,pk=pk)                # Витягуємо конкретний товар із бд

    comments = Comments.objects.filter(product=product)        # + коментарі до даного товару

    if request.method == 'POST':
        form = CommentsForm(request.POST)
        if not request.user.is_authenticated:  # ← додатковий захист щоб незареєстровані користувачі не могли писати коментарі
            return redirect('login')

        if form.is_valid():
            comment = form.save(commit=False)  # не зберігаємо одразу           # дана форма приймає тільки текст коментаря тому ми також
            comment.product = product  # прив'язуємо до товару
            comment.user = request.user  # прив'язуємо до користувача
            comment.save()  # тепер зберігаємо
            return redirect('product_detail', pk=product.pk)  # повертаємось на ту ж сторінку
    else:
        form = CommentsForm()

    return render(request, 'catalog_products/product_detail.html', {'product': product , 'comments': comments , 'form': form})