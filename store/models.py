# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.core.urlresolvers import reverse


class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")
    isPublish = models.BooleanField(default=False, verbose_name="Опубликован?")

    class Meta:
        abstract = True


class Formula(Base):
    text = models.CharField(max_length=200, verbose_name="Текст формулы",
                            help_text="Вместо переменной цены МВидео впиши ## (две решетки), например, (## - 1000) * 0.95")
    durationFrom = models.PositiveIntegerField(verbose_name="Минимальная цена",
                                               help_text="Ценовой минимум, при котором будет действовать формула")
    durationTo = models.PositiveIntegerField(verbose_name="Максимальная цена",
                                             help_text="Ценовой максимум, при котором будет действовать формула")

    class Meta:
        verbose_name = 'Формула'
        verbose_name_plural = 'Формулы'

    def __unicode__(self):
        return str(self.durationFrom) + " - " + str(self.durationTo) + " | " + self.text


# Модель категории
class Category(Base):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    parent = models.ForeignKey('self', blank=True, null=True, verbose_name="Родитель", related_name="children")
    image = models.ImageField(upload_to='media/categories/%Y/%m/%d/', blank=True, verbose_name="Изображение категории")
    formules = models.ManyToManyField(Formula, verbose_name="Формулы", related_name="categories")
    delivery_cost = models.PositiveIntegerField(verbose_name="Стоимость доставки")

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('store:ProductListByCategory', args=[self.slug])


# Модель продукта
class Product(Base):

    category = models.ForeignKey(Category, related_name='products', verbose_name="Категория")
    mCode = models.CharField(max_length=8, verbose_name="Артикул МВидео")
    mUrl = models.URLField(verbose_name="Ссылка на сайт МВидео")
    typePrefix = models.CharField(max_length=200, db_index=True, verbose_name="Тип товара", null=True)
    vendor = models.CharField(max_length=200, db_index=True, verbose_name="Производитель", null=True)
    model = models.CharField(max_length=200, db_index=True, verbose_name="Модель", null=True)
    image = models.ImageField(upload_to='media/products/%Y/%m/%d/', blank=True, verbose_name="Изображение товара")
    description = models.TextField(blank=True, verbose_name="Описание", null=True)
    price = models.PositiveIntegerField(verbose_name="Цена", null=True)
    mPrice = models.PositiveIntegerField(verbose_name="Цена в МВидео", null=True)
    inStock = models.BooleanField(default=False, verbose_name="В наличии?")

    class Meta:
        ordering = ['typePrefix', 'vendor', 'model']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __unicode__(self):
        return self.typePrefix + ' ' + self.vendor + ' ' + self.model

    def get_absolute_url(self):
        return reverse('store:ProductDetail', args=[self.category.slug, self.id])


class Params(Base):
    name = models.CharField(max_length=200, verbose_name="Наименование")
    value = models.CharField(max_length=200, verbose_name="Значение")
    product = models.ForeignKey(Product, related_name="params", verbose_name="Товар")

    class Meta:
        verbose_name = 'Характеристика товара'
        verbose_name_plural = 'Характеристики товара(ов)'

    def __unicode__(self):
        return self.name


