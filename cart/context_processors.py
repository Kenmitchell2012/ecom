from .cart import Cart

#Create context processor
def cart(request):
    #  Return default data of cart
    return {'cart': Cart(request)}