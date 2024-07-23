
from django.http import HttpResponse
from cart.models import Cart
from shop.models import Products
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
import razorpay
from django.views.decorators.csrf import csrf_exempt
import pkg_resources
from .models import Payment,Order_table
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
# Create your views here.

@login_required
def add_to_cart(request,i):
    p=Products.objects.get(id=i)
    u=request.user
    try:
        cart=Cart.objects.get(user=u,product=p)
        if(p.stock>0):
            cart.quantity +=1
            cart.save()
            p.stock -=1
            p.save()
    except:
        if (p.stock):
            cart=Cart.objects.create(product=p,user=u,quantity=1)
            cart.save()
            p.stock -=1
            p.save()
    return redirect('cart:viewcart')

@login_required
def cart_view(request):
    u=request.user
    cart=Cart.objects.filter(user=u)
    total=0
    for i in cart:
        total=total+(i.quantity * i.product.price)
    return render(request,'cart_view.html',{'cart':cart,'total':total})

def cart_decrement(request,i):
    p=Products.objects.get(id=i)
    u=request.user
    try:
        cart=Cart.objects.get(user=u,product=p)
        if(cart.quantity>1):
            cart.quantity -=1
            cart.save()
            p.stock +=1
            p.save()
        else:
            cart.delete()
            p.stock+=1
            p.save()
    except:
        pass

    return redirect ('cart:viewcart')

def cart_delete(request,i):
    p=Products.objects.get(id=i)
    u=request.user
    cart = Cart.objects.get(user=u, product=p)
    cart.delete()
    p.stock +=cart.quantity
    p.save()
    return redirect('cart:viewcart')

def order(request):
    if (request.method=='POST'):
        phone=request.POST['ph']
        address=request.POST['a']
        pin=request.POST['p']
        u = request.user
        c=Cart.objects.filter(user=u)
        total=0
        for i in c:
            total=total+(i.quantity*i.product.price)
        total=int(total*100)
        # print(type(total))
        # create razorpay client
        client=razorpay.Client(auth=('rzp_test_JT7cbV84p0vQBq','gk94x1uxg3vqUeEDEd5Jmd30'))
        # #create order
        response_payment=client.order.create(dict(amount=total,currency='INR'))
        print(response_payment)
        # response_payment.save()
        order_id=response_payment['id']
        order_status=response_payment['status']
        if order_status=='created':
            p=Payment.objects.create(name=u.username,amount=total,order_id=order_id)
            p.save()
            for i in c:
                o=Order_table.objects.create(user=u,product=i.product,address=address,phone=phone,pin=pin,no_of_items=i.quantity,order_id=order_id)
                o.save()
            response_payment['name']=u.username
        return render(request,'payment.html',{'payment':response_payment})
    return render(request,'order.html')

@csrf_exempt
def payment_status(request,u):
    print(request.user.is_authenticated)
    # u = request.user
    if not request.user.is_authenticated:
        user = User.objects.get(username=u)
        login(request,user)
        print(request.user.is_authenticated)
    if request.method=='POST':
        response=request.POST
        # print(response)
        # print(u)
        payment_id=response.get('razorpay.payment_id')
        order_id=response.get('razorpay_order_id')
        signature=response.get('razorpay_signature')
        param_dict={
            'razorpay_order_id':response['razorpay_order_id'],
            'razorpay_payment_id':response['razorpay_payment_id'],
            'razorpay_signature':response['razorpay_signature']
        }
        client=razorpay.Client(auth=('rzp_test_JT7cbV84p0vQBq','gk94x1uxg3vqUeEDEd5Jmd30'))
        try:
            status=client.utility.verify_payment_signature(param_dict)
            # print(status)
            ord=Payment.objects.get(order_id=response['razorpay_order_id'])
            ord.razorpay_payment_id=response['razorpay_payment_id']
            ord.paid=True
            ord.save()
            u=User.objects.get(username=u)
            # print(u.username)
            c=Cart.objects.filter(user=u)
            o=Order_table.objects.filter(user=u,order_id=response['razorpay_order_id'])
            # print(o)
            for i in o:
                i.payment_status = 'paid'
                i.save()
            c.delete()
            return render(request,'payment_status.html',{'status':True})
        except:
            return render(request, 'payment_status.html', {'status':False})
    return render(request,'payment_status.html')

@login_required
def yourorders(request):
    u=request.user
    order=Order_table.objects.filter(user=u,payment_status='paid')
    return render(request,'orderview.html',{'order':order,'u':u.username})