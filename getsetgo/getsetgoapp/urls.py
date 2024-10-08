"""
URL configuration for getsetgo project.

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
from .import views as v
from .views import create_order,payment_success,user_rides

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',v.home,name='home'),
    path('vlist',v.vehicle_list,name='vlist1'),
    path('signup',v.signup,name='add_user'),
    path('booking',v.booking,name='booking'),
    path('login',v.login_view,name='login'),
    path('logout',v.logout_view,name='logout'), 
    path('booking/<int:vehicle_id>/', v.booking_form, name='booking_form'),
    path('vehicles/', v.vehicle_list, name='vehicle_list'),
    path('create_order/', create_order, name='create_order'),
    path('payment-success/',payment_success, name='payment_success'),
    path('payment/callback/<int:booking_id>/', v.payment_callback, name='payment_callback'),
    path('your_rides', user_rides, name='your_ride'),
]

