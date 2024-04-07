from django.shortcuts import render
from catalog.models import Product


def index(request):
    product_list = Product.objects.all()
    context = {
        'object_list': product_list,
        'title': 'Главная'
    }
    return render(request, 'main/home.html', context)


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'{name} ({phone}): {message}')

    context = {
        'title': 'Контакты'
    }
    return render(request, 'main/contacts.html', context)


def product(request):
    context = {
        'title': 'Продукты'
    }
    return render(request, 'main/product.html', context)
