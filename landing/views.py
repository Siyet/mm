# -*- coding: utf-8 -*-
from django.shortcuts import render


# Страница с товарами
def Landing(request):
    return render(request, 'landing/landing.html', {
        "pass": "pass"
    })
