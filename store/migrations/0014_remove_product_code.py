# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-10-13 16:20
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_auto_20171013_1909'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='code',
        ),
    ]
