# -*- coding: utf-8 -*-
# from celery.task import task
# import re
# import requests
# from models import Product


# @task(ignore_result=True, max_retries=1, default_retry_delay=10)
# def update_prices():
#     for p in Product.objects.all():
#         p.code = p.get_vendor_code()
#         p.save()
#         try:
#             r_text = requests.get(p.mUrl).text
#         except Exception:
#             p.isPublish = False
#             p.save()
#             print u"Product with ID " + p.code + u" error request"
#             continue
#         if re.search(u'Товар распродан', r_text) or re.search(u'Cтраница не найдена\.', r_text):
#             p.isPublish = False
#             p.save()
#             print u"Product with ID " + p.code + u" page not found or product sold out"
#             continue
#         try:
#             id = re.search("'productId': '([0-9]+)'", r_text).group(1)
#             if p.mCode and id != p.mCode:
#                 p.isPublish = False
#                 p.save()
#                 print u"Product with ID " + p.code + u" has mCode ("+p.mCode+u") but not equal with external ID ("+id+u")"
#                 continue
#             elif p.mCode != id:
#                 p.mCode = id
#                 p.save()
#         except Exception:
#             p.isPublish = False
#             p.save()
#             print u"Product with ID " + p.code + u" not found id"
#             continue
#         try:
#             price = re.search("'productPriceLocal': '([0-9]+)\.", r_text).group(1)
#             p.mPrice = int(price)
#         except Exception:
#             p.isPublish = False
#             p.save()
#             print u"Product with ID " + p.code + u" not found price"
#             continue
#         try:
#             formula = p.category.formules.filter(durationFrom__lt=p.mPrice, durationTo__gt=p.mPrice)[0]
#             p.price = eval(formula.text.replace("##", str(
#                 p.mPrice)))  # TODO добавить проверку на отсутствие символов отличных от цифр, +, -, *, /, (, ), ., #
#         except Exception:
#             p.price = p.mPrice
#         p.isPublish = True
#         p.inStock = True
#         p.save()
