from cart.models import Cart
def Total(request):
    u=request.user
    count=0
    if request.user.is_authenticated:
        try:
            item=Cart.objects.filter(user=u)
            count=count+item.count()
        except:
            count=1
    return {'count':count}
