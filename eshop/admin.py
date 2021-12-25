from django.contrib import admin
from .models import Product,Homepageslider,Orders,OrderItem,CartOrder
# Register your models here.

admin.site.register(Product)
admin.site.register(Homepageslider)
admin.site.register(Orders)
admin.site.register(OrderItem)
admin.site.register(CartOrder)