# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-08 19:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_auto_20170108_2212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='comments_in',
            field=models.TextField(blank=True, default=b'', verbose_name=b'\xd0\x9a\xd0\xbe\xd0\xbc\xd0\xbc\xd0\xb5\xd0\xbd\xd1\x82\xd0\xb0\xd1\x80\xd0\xb8\xd0\xb9 \xd0\xb2\xd0\xbd\xd1\x83\xd1\x82\xd1\x80\xd0\xb5\xd0\xbd\xd0\xbd\xd0\xb8\xd0\xb9'),
        ),
    ]