"""ecom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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

from django.urls import path ,include
from .views import *
from django.contrib.auth import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('homepage',prod.as_view(),name='product'),
    path('slider',Slide.as_view(),name='slider'),
    path('',Home.as_view(),name='slider'),
    path('<int:pk>',Productdetail.as_view(),name='productdetail'),
    path('orders',Order.as_view(),name='orders'),
    path('orders/<int:pk>',Orderdetail.as_view(),name='orders'),
    path('accounts/profile/',Profileview.as_view(),name='profile'),
    path('accounts/password_change/', views.PasswordChangeView.as_view(template_name='profile.html'), name='profile'),
    path('search', prod_search),
    path('add_to_cart/<int:pk>',add_to_cart),
    path('cart',order_detail),
    path('delete/<int:pk>',delete_order),
    path('prod_images',homepage_slider),
    path('pay',homepage),
    path('cre',Creat_prod.as_view(),name='create_prod'),
    path('sample/<int:pk>',Update_prod.as_view(),name='update_prod'),
    path('prod/<int:pk>',detail_view.as_view(),name='detail')

]

