from django.shortcuts import render
from django.db.models import Q
from shop.models import Products
# Create your views here.
def search_products(request):
    items=None
    query=''
    if request.method=='POST':
        query=request.POST['s']
        if query:
            items=Products.objects.filter(Q(name__icontains=query))
    return render(request,'search.html',{'items':items,'query':query})