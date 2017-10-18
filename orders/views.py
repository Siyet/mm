# -*- coding: utf-8 -*-
from django.shortcuts import render
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from store.models import Category
# from .tasks import OrderCreated


def OrderCreate(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()
            # Асинхронная отправка сообщения
            # OrderCreated(order.id)
            return render(request, 'orders/order/created.html', {'cart': cart,  'form': form, 'order': order})

    form = OrderCreateForm()
    categories = Category.objects.filter(isPublish=True)
    return render(request, 'orders/order/create.html', {'cart': cart,
                                                        'form': form,
                                                        'categories': categories})


def get_torg12(request, id):
    order = Order.objects.get(id=id)
    return render(request, 'orders/order/torg12.html', {'order': order, 'delivery_num': order.items.count() + 1})
