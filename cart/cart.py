
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