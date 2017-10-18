# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_field = ['product']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_items', "comments", "comments_in", 'phone', 'name',
                     'get_delivery_cost', 'get_total_cost', 'address','email', 'paid']
    list_filter = ['paid', 'created', 'updated']
    list_editable = ['paid']
    inlines = [OrderItemInline]

    def get_items(self, obj):
        result = ""
        for item in obj.items.all():
            result += str(item.product) + " (" + str(item.quantity) + ' шт.);\n'
        return result

    get_items.short_description = u'Заказ'
    get_items.admin_order_field = 'item__id'

admin.site.register(Order, OrderAdmin)
