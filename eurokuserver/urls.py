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
from price import views as price_views
from control import views as control_views

urlpatterns = [
    url(r'^api/1.0/galdera', api.question, name="euroku_question"),
    url(r'^api/1.0/prices/public$', api.publicprices, name="euroku_publicprices"),
    url(r'^api/1.0/prices/(?P<price_key>[a-zA-Z0-9]+)', api.price, name="euroku_price"),
    url(r'^api/1.0/prices$', api.prices, name="euroku_prices"),
    url(r'^api/1.0/profile', api.profile, name="euroku_profile"),
    url(r'^api/1.0/register', api.register, name="euroku_register"),
    url(r'^sariak', price_views.search, name="euroku_search"),
    url(r'^login', control_views.login, {"template_name": "login.html"}, name="euroku_login"),
    url(r'^admin/load_questions$', control_views.add_questions, name="euroku_add_questions"),
    url(r'^admin/', include(admin.site.urls)),
]
