# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Category, Product, Formula, Params


# Модель категории
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'slug', 'id']
    prepopulated_fields = {'slug': ('name', )}


class ParamsInline(admin.TabularInline):
    model = Params


class PriceFilter(admin.SimpleListFilter):
    title = u'Цена'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'price_cat'

    def lookups(self, request, model_admin):
        formules = Formula.objects.filter(isPublish=True)
        res = []
        for item in formules:
            res.append((item.id, u"от " + str(item.durationFrom) + u" до " + str(item.durationTo)))
        print res
        return res

    def queryset(self, request, queryset):
        print self.value()
        if self.value():
            formula = Formula.objects.get(id=self.value())
            return queryset.filter(price__lt=formula.durationTo, price__gt=formula.durationFrom)
        else:
            return queryset.all()


# Модель товара
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'mCode', '__unicode__', 'price', 'inStock', 'isPublish', 'updated_at']
    list_filter = [PriceFilter, 'created_at', 'updated_at', 'inStock', 'isPublish']
    list_editable = ['inStock', 'isPublish']
    search_fields = ['id', 'mCode', 'typePrefix', 'vendor', 'model']
    inlines = [ParamsInline]
    save_on_top = True


# Модель товара
class FormulaAdmin(admin.ModelAdmin):
    list_display = ['text', 'durationFrom', 'durationTo', 'updated_at']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Formula, FormulaAdmin)
