from shop.models import Category

def Links(request):
    c=Category.objects.all()
    return{'links':c}