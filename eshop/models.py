import uuid
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Product(models.Model):
    choices=(
         ('yes',True),
         ('no',False)
     )
    name= models.CharField(max_length=124)
    desc = models.TextField(max_length=1245)
    sku= models.CharField(max_length=124)
    prod_images= models.ImageField(upload_to='upload/')
    price = models.IntegerField(max_length=1234,default=25,null=True)
    is_featured=models.BooleanField(choices=choices,default=False)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Homepageslider(models.Model):
    image_text=models.CharField(max_length=1245)
    slider_image=models.ImageField(upload_to='slider')
    offer_text=models.CharField(max_length=45660)

    def __str__(self):
        return self.image_text

class OrderItem(models.Model):
    product=models.OneToOneField(Product,on_delete=models.SET_NULL,null=True)
    is_ordered= models.BooleanField(default=False)
    date_added=models.DateTimeField(auto_now=True)
    date_ordered=models.DateTimeField(null=True)

    def __str__(self):
        return self.product.name

class CartOrder(models.Model):
    ref_code = models.CharField(max_length=15)
    owner = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    is_ordered=models.BooleanField(default=False)
    items = models.ManyToManyField(OrderItem)
    date_ordered =models.DateTimeField(auto_now=True)


    def get_cart_items(self):
        return self.items.all()

    def get_cart_total(self):
        total =0
        for item in self.items.all():
            total=total+ item.product.price
        return total

    def __str__(self):
        return '{0} - {1}'.format(self.owner,self.ref_code)

class Orders(models.Model):
    order_date=models.DateTimeField(auto_now_add=True,null=True)
    order_id = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True, editable=False)
    user = models.ForeignKey(User,on_delete=models.PROTECT)
    product_name=models.ForeignKey(Product,on_delete=models.PROTECT)

    # def __int__(self):
    #     return self.order_id



# class Cart(models.Model):
#     name = models.CharField(max_length=1234)
#     user=models.ForeignKey(User,on_delete=models.CASCADE)
#     created_at=models.DateTimeField(auto_now=True)
#     prod_name=models.ForeignKey(Product,on_delete=models.CASCADE)
#     # price=models.ForeignKey(Product.price,on_delete=models.CASCADE)
#     quantity = models.IntegerField(max_length=123)
#     cart_id = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True, editable=False)
#
#     def __str__(self):
#         return self.name
