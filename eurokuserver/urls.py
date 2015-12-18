"""eurokuserver URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from . import api

urlpatterns = [
    url(r'^api/1.0/galdera', api.question, name="euroku_question"),
    url(r'^api/1.0/prices/public', api.publicprices, name="euroku_publicprices"),
    url(r'^api/1.0/prices', api.prices, name="euroku_prices"),
    url(r'^api/1.o/prices/(P<price_key>[A-B0-9]+)', api.price, name="euroku_price"),
    url(r'^api/1.0/profile', api.profile, name="euroku_profile"),
    url(r'^admin/', include(admin.site.urls)),
]
