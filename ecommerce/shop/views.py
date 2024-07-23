from django.shortcuts import render,redirect
from shop.models import Category,Products
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.

def category(request):
    item=Category.objects.all()
    return render(request,'category.html',{'item':item})
def products(request,m):
    # item=Category.objects.all()
    # product=Products.objects.filter(category=m)
    # or
    product=Category.objects.get(id=m)
    item=Products.objects.filter(category=product)
    # or
    # product=Products.objects.filter(category_id=m)
    # or
    # product=Products.objects.filter(category_name=m)
    return render(request,'products.html',{'product':product,'item':item})

def product_details(request,m):
    product=Products.objects.get(id=m)
    return render(request,'productdetails.html',{'product':product})


def register(request):
    if(request.method=='POST'):
        u=request.POST['u']
        p=request.POST['p']
        cp=request.POST['cp']
        e=request.POST['e']
        fn=request.POST['fn']
        ln=request.POST['ln']
        if(cp==p):
            user=User.objects.create_user(username=u,password=p,first_name=fn,last_name=ln,email=e)
            user.save()
            return redirect('userlogin')
    return render(request,'register.html')

def userlogin(request):
    if(request.method=='POST'):
        u=request.POST['u']
        p=request.POST['p']
        user=authenticate(username=u,password=p)
        if user:
            login(request,user)
            return redirect('category')
        else:
            messages.error(request,'Invalid credentials')
    return render(request,'login.html')

def userlogout(request):
    logout(request)
    return redirect('userlogin')