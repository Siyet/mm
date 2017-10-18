# -*- coding: utf-8 -*-
from decimal import Decimal
from django.conf import settings
from store.models import Product


class Cart(object):
    def __init__(self, request):
        # Инициализация корзины пользователя
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Сохраняем корзину пользователя в сессию
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    # Добавление товара в корзину пользователя или обновление количества товара
    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        if product.inStock and product.isPublish:
            if product_id not in self.cart:
                self.cart[product_id] = {'quantity': 0,
                                         'price': str(product.price)}
            if update_quantity:
                self.cart[product_id]['quantity'] = quantity
            else:
                self.cart[product_id]['quantity'] += quantity
        else:
            if product_id in self.cart:
                del self.cart[product_id]
        self.save()

    # Сохранение данных в сессию
    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        # Указываем, что сессия изменена
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

            # Итерация по товарам

    def __iter__(self):
        for key in self.cart.keys():
            try:
                self.cart[str(key)]['product'] = Product.objects.get(id=int(key))
            except Product.DoesNotExist:
                del self.cart[key]

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    # Количество товаров
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def get_delivery_cost(self):
        delivery_cost = 0
        quantity = -1
        for item in self.cart.values():
            quantity += item['quantity']
            if delivery_cost < item['product'].category.delivery_cost:
                delivery_cost = item['product'].category.delivery_cost
        if quantity > 0:
            delivery_cost += 100 * quantity
        if delivery_cost > 2000:
            delivery_cost = 2000
        return delivery_cost

    def get_order_price(self):
        return self.get_total_price() + self.get_delivery_cost()

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
