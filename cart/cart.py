from store.models import Product

class Cart():
    def __init__(self, request):
        self.session = request.session

        # Get the current session key if available
        cart = self.session.get('session_key')

        # If the user is new, create a new session key
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        # make carrt available on all pages of site
        self.cart = cart

    def add(self, product):
        product_id = str(product.id)

        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = {'price': str(product.price)}

        self.session.modified = True
        
    def __len__(self):
        return len(self.cart)
    
    def get_prods(self):
        #get ids of all products in cart
        product_ids = self.cart.keys()
        #use ids to lookup products
        products = Product.objects.filter(id__in=product_ids)
        # return products
        return products