"""
URL configuration for lab1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path


import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from templates import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', views.hello),
    path('', views.GetServices, name = 'home_page_url'),
    path('service/<int:id>/', views.GetService, name = 'service_url'),
    path('basket/', views.GetBasket, name = 'basket_url'),
    path('calculation/<int:id>/', views.GetCalculation, name='calculation'),
]
