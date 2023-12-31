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

    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)

        # logic
        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)

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
    
    def get_quants(self):
        quantities = self.cart
        return quantities
    
    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)

        # debugging
        print(f"Updating cart for product ID: {product_id}, Quantity: {product_qty}")

        #get cart
        ourcart = self.cart
        # update cart/dictionary
        ourcart[product_id] = product_qty

        self.session.modified = True
        thing = self.cart
        return thing