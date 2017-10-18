# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# # Модель слайдера
# class Slider(Base):
#     title = models.CharField(max_length=200)
#     description = models.TextField(blank=True, null=True, verbose_name="Описание")
#     image = models.ImageField(upload_to='media/categories/%Y/%m/%d/', blank=True, verbose_name="Изображение категории")
#     formules = models.ManyToManyField(Formula, verbose_name="Формулы", related_name="categories")
#     delivery_cost = models.PositiveIntegerField(verbose_name="Стоимость доставки")

#     class Meta:
#         ordering = ['name']
#         verbose_name = 'Категория'
#         verbose_name_plural = 'Категории'

#     def __unicode__(self):
#         return self.name

#     def get_absolute_url(self):
#         return reverse('store:ProductListByCategory', args=[self.slug])

# Create your models here.
