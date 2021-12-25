from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import ListView ,TemplateView,DetailView,CreateView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
#from ecom import settings
from .models import *
from django.views.decorators.csrf import csrf_exempt
import razorpay
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

class prod(ListView):
    model = Product
    template_name = 'products.html'
    context_object_name = 'Products'



class  Profileview(TemplateView):
    template_name = 'registration/profile.html'


class Slide(ListView):
    model = Homepageslider
    template_name = 'slider.html'


class Home(TemplateView):

    template_name = 'slider.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['Products'] = Product.objects.all()
        context['Homepageslider'] = Homepageslider.objects.all()
        return context


class Productdetail(DetailView):
    template_name = 'Product_detail.html'
    model = Product
    # queryset = Product.objects.all()
    context_object_name = 'Product'



class Order(LoginRequiredMixin,ListView):
    template_name ="orders.html"
    context_object_name = 'Orders'

    def get_queryset(self):
        print()
        return Orders.objects.filter(user=self.request.user)





class Orderdetail(LoginRequiredMixin,DetailView):
    template_name ="Order_detail.html"
    context_object_name = 'Order'

    def get_queryset(self):
        return Orders.objects.filter(user=self.request.user)


def prod_search(request):
    q=request.GET['q']
    prod_list= Product.objects.filter(name__icontains=q)
    context={
        'Products': prod_list

    }
    print(prod_list)
    return render(request,'search.html',context=context)



@login_required(login_url='/login')

def add_to_cart(request,pk):
    user=request.user
    product = Product.objects.filter(id=pk).first()
    order_item,status = OrderItem.objects.get_or_create(product=product)
    user_order,status=CartOrder.objects.get_or_create(owner=user,is_ordered=False)
    user_order.items.add(order_item)
    user_order.ref_code="1235566"
    user_order.save()

    messages.info(request,"item added to Cart")
    return redirect('/')


@login_required(login_url='/login')
def delete_order(request,pk):
    item_to_delete = OrderItem.objects.filter(pk=pk)
    # it=CartOrder.objects.filter(items=item_to_delete)
    # print(it)


    print(item_to_delete)
    if item_to_delete.exists():
        item_to_delete.delete()
        print("done")
        messages.info(request,'ITEM deleted')
    return redirect('/cart')


def get_user_pending_order(request):
    user=request.user
    order=CartOrder.objects.filter(owner=user,is_ordered=False)
    if order.exists():
        return order[0]
    return 0

@login_required(login_url='/login')
def order_detail(request):
    existing_order=get_user_pending_order(request)
    context={
        'order':existing_order
    }
    return render(request,'cart.html',context)

@login_required(login_url='/login')
def checkout(request):
    existing_order=get_user_pending_order(request)
    context={
        'order':existing_order
    }
    return render(request,'checkout.html',context)



def homepage_slider(request):
    slider_data= Homepageslider.objects.all()
    context={
        'Homepageslider':slider_data
    }

    return render(request,'prod_images.html',context=context)

#razorpay settings

razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


@csrf_exempt
def homepage(request):
    currency = 'INR'

    amount = 20000  # Rs. 200

    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,currency=currency,
                                                           payment_capture='1'))

    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    #callback_url = 'paymenthandler/'

    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = 'INR'
    #context['callback_url'] = callback_url
    if request.method == "POST":
        payment_id = request.POST.get('razorpay_payment_id', '')
        razorpay_order_id = request.POST.get('razorpay_order_id', '')
        signature = request.POST.get('razorpay_signature', '')
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }

        # verify the payment signature.
        result = razorpay_client.utility.verify_payment_signature(
            params_dict)
        razorpay_client.payment.capture(payment_id, amount)
        return HttpResponse("payment done")


    return render(request, 'pay.html', context=context)

from .forms import prodform

class Creat_prod(CreateView):
    model = Product
    fields = ('__all__')
    #form_class = prodform
    template_name = 'prod_create.html'
    success_url = '/cre'

class Update_prod(UpdateView):
    model = Product
    fields = ('__all__')
    template_name='prod_create.html'
    success_url = '/cre'

class detail_view(DetailView):
    template_name = 'Product_detail.html'
    model = Product
    #model = Product
    # queryset = Product.objects.all()
    context_object_name = 'Product'