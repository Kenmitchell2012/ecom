from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse

# Create your views here.

def cart_summary(request):
    username = request.user.username
    return render(request, 'cart_summary.html', {'username': username})

def cart_add(request):
    cart = Cart(request)
    # test for post
    if request.POST.get('action') == 'post':
        # get items
        product_id = int(request.POST.get('product_id'))
        # lookup product in database
        product = get_object_or_404(Product, id=product_id)

        # save to session
        cart.add(product=product)
        
        # get cart quantity
        cart_quantity = cart.__len__()

        #return response
        # response = JsonResponse({'Product Name': product.name})
        response = JsonResponse({'qty': cart_quantity})

        return response

def cart_delete(request):
    pass

def cart_update(request):
    pass
