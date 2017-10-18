# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from .models import Category, Product, Formula, Params
from cart.forms import CartAddProductForm
import requests
import json
import re
from lxml import etree
from datetime import datetime, timedelta
from django.core.files import File
# from tasks import update_prices


# Страница с товарами
def ProductList(request, category_slug=None):
    category = None
    categories = Category.objects.filter(isPublish=True)
    products = Product.objects.filter(isPublish=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'store/product/list.html', {
        'category': category,
        'categories': categories,
        'products': products
    })


# Страница товара
def ProductDetail(request, category_slug, id):
    categories = Category.objects.filter(isPublish=True)
    product = get_object_or_404(Product, id=id, isPublish=True)
    cart_product_form = CartAddProductForm()
    return render_to_response('store/product/detail.html',
                             {'product': product,
                              'categories': categories,
                              'cart_product_form': cart_product_form})


def update_prices(request):
    if request.user.is_superuser:
        prod_all = Product.objects.all().order_by("updated_at")
        log = ""
        for p in prod_all:
            try:
                r_text = requests.get(p.mUrl).text
            except Exception:
                p.isPublish = False
                p.save()
                log += u"Product with ID " + str(p.id) + u" error request\n"
                continue
            if re.search(u'Товар распродан', r_text) or re.search(u'Cтраница не найдена\.', r_text):
                p.isPublish = False
                p.save()
                log += u"Product with ID " + str(p.id) + u" page not found or product sold out\n"
                continue
            try:
                id = re.search("'productId': '([0-9]+)'", r_text).group(1) if re.search("'productId': '([0-9]+)'", r_text) else re.search("c\-product\-code\">([0-9]+)", r_text).group(1)
                if p.mCode and id != p.mCode:
                    p.isPublish = False
                    p.save()
                    log += u"Product with ID " + str(p.id) + u" has mCode ("+p.mCode+u") but not equal with external ID ("+id+u")\n"
                    continue
                elif p.mCode != id:
                    p.mCode = id
                    p.save()
            except Exception:
                p.isPublish = False
                p.save()
                log += u"Product with ID " + str(p.id) + u" not found id\n"
                continue
            try:
                price = re.search("'productPriceLocal': '([0-9]+)\.", r_text).group(1) if re.search("'productPriceLocal': '([0-9]+)\.", r_text) else re.sub("[^0-9]+", "", re.search("c-pdp-price__current\">([^<]+)", r_text).group(1))
                p.mPrice = int(price)
            except Exception:
                p.isPublish = False
                p.save()
                log += u"Product with ID " + str(p.id) + u" not found price\n"
                continue
            try:
                formula = p.category.formules.filter(durationFrom__lte=p.mPrice, durationTo__gte=p.mPrice)[0]
                p.price = eval(formula.text.replace("##", str(
                    p.mPrice)))  # TODO добавить проверку на отсутствие символов отличных от цифр, +, -, *, /, (, ), ., #
            except Exception:
                p.price = p.mPrice
            p.isPublish = True
            p.inStock = True
            p.save()
    else:
        return HttpResponseRedirect('/')

    return render_to_response('store/report.html', {})


def escape_xml(str):
    return str.replace('&','&amp;').replace('"','&quot;').replace('\'','&apos;').replace('>','&gt;').replace('<','&lt;')


def get_products_yml(request):
    data = '<?xml version="1.0" encoding="utf-8"?>'
    xml = etree.Element("yml_catalog", date=datetime.now().strftime('%Y-%m-%d %H:%M'))
    shop = etree.SubElement(xml, "shop")
    etree.SubElement(shop, "name").text = "Macromag"
    etree.SubElement(shop, "company").text = u"ООО &quot;ЭЗРА&quot;"
    etree.SubElement(shop, "url").text = "http://macromag.ru"
    currencies = etree.SubElement(shop, "currencies")
    etree.SubElement(currencies, "currency", id="RUR", rate="1")
    categories = etree.SubElement(shop, "categories")
    for cat in Category.objects.filter(isPublish=True):
        if cat.parent and cat.parent.isPublish:
            etree.SubElement(categories, "category", id=str(cat.id), parentId=str(cat.parent.id)).text = escape_xml(cat.name)
        elif not cat.parent:
            etree.SubElement(categories, "category", id=str(cat.id)).text = escape_xml(cat.name)
    delivery_options = etree.SubElement(shop, "delivery-options")
    etree.SubElement(delivery_options, "option", cost="2000", days="1-3")
    offers = etree.SubElement(shop, "offers")
    for product in Product.objects.filter(isPublish=True, category__isPublish=True):
        if (product.category.parent and product.category.parent.isPublish) or not product.category.parent:
            offer = etree.SubElement(offers, "offer",
                                     id=str(product.id),
                                     type="vendor.model",
                                     available="true" if product.inStock else "false")
            etree.SubElement(offer, "url").text = "http://macromag.ru" + product.get_absolute_url()
            etree.SubElement(offer, "price").text = str(product.price)
            etree.SubElement(offer, "currencyId").text = "RUR"
            etree.SubElement(offer, "categoryId").text = str(product.category.id)
            etree.SubElement(offer, "picture").text = "http://macromag.ru" + product.image.url
            #etree.SubElement(offer, "pickup").text = "false"
            etree.SubElement(offer, "delivery").text = "true"
            do = etree.SubElement(offer, "delivery-options")
            etree.SubElement(do, 'option', cost=str(product.category.delivery_cost), days="1-3")
            etree.SubElement(offer, "typePrefix").text = escape_xml(product.typePrefix)
            etree.SubElement(offer, "vendor").text = escape_xml(product.vendor)
            etree.SubElement(offer, "model").text = escape_xml(product.model)
            etree.SubElement(offer, "manufacturer_warranty").text = "true"
            if product.params.count > 0:
                for param in product.params.all():
                    etree.SubElement(offer, "param", name=param.name).text = escape_xml(param.value)

    return HttpResponse(data + etree.tostring(xml), content_type="application/xml")