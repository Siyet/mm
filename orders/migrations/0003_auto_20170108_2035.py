# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-08 17:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_order_phone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='city',
        ),
        migrations.RemoveField(
            model_name='order',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='order',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='order',
            name='postal_code',
        ),
        migrations.AddField(
            model_name='order',
            name='name',
            field=models.CharField(default=1, max_length=200, verbose_name=b'\xd0\x98\xd0\xbc\xd1\x8f'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.CharField(max_length=250, verbose_name=b'\xd0\x90\xd0\xb4\xd1\x80\xd0\xb5\xd1\x81 \xd0\xb4\xd0\xbe\xd1\x81\xd1\x82\xd0\xb0\xd0\xb2\xd0\xba\xd0\xb8'),
        ),
    ]
