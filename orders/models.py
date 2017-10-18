# -*- coding: utf-8 -*-
from django.db import models
from store.models import Product


class Order(models.Model):
    name = models.CharField(verbose_name='Имя', max_length=200)
    email = models.EmailField(verbose_name='Email')
    address = models.CharField(verbose_name='Адрес доставки', max_length=250, blank=True)
    phone = models.CharField(verbose_name='Телефон', max_length=20)
    created = models.DateTimeField(verbose_name='Создан', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Обновлен', auto_now=True)
    paid = models.BooleanField(verbose_name='Оплачен', default=False)
    comments = models.TextField(verbose_name="Комментарий", blank=True, default="")
    comments_in = models.TextField(verbose_name="Комментарий внутренний", blank=True, default="")

    class Meta:
        ordering = ('-created', )
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return str(self.id)

    def get_delivery_cost(self):
        delivery_cost = 0
        quantity = -1
        for item in self.items.all():
            quantity += item.quantity
            if delivery_cost < item.product.category.delivery_cost:
                delivery_cost = item.product.category.delivery_cost
        if quantity > 0:
            delivery_cost += 100 * quantity
            #     12.06.2017 22:30, Эл сказал убрать ограничение в 2000 рублей
            # if delivery_cost > 2000:
            #     delivery_cost = 2000
        return delivery_cost

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all()) + self.get_delivery_cost()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items')
    product = models.ForeignKey(Product, related_name='order_items')
    price = models.DecimalField(verbose_name='Цена', max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(verbose_name='Количество', default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
