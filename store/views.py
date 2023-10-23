from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Cart, Product, CartProduct
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import SignUpForm
from django.db import models

# Create your views here.

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def about(request):
    return render(request, 'about.html', {})


def login_user(request):
    if request.method == "POST":
        usernames = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=usernames, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("Welcome, " + user.username))
            return redirect('home')

        else:
            messages.success(request, ("There was a problem logging in"))
            return redirect('login')
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ('You have been logged out'))
    return redirect('home')
 
def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            #login user
            user = authenticate(username= username, password=password)
            login(request, user)
            messages.success(request, 'You have successfully created a account!!')
            return redirect('home')
        else:
            messages.error(request, 'There was an error registering, please try again')
            return redirect('register')
    else:
        return render(request, 'register.html', {'form': form})
    
def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product': product})

def add_to_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Check if the product is already in the cart
    cart_product, created = CartProduct.objects.get_or_create(cart=cart, product=product)
    
    # If the cart_product was just created (i.e., it didn't exist previously), set the quantity to 1.
    if created:
        cart_product.quantity = 1
    else:
        # If the cart_product already existed, increase the quantity by 1.
        cart_product.quantity += 1

    cart_product.save()
    return redirect('view_cart')



def calculate_cart_total(cart):
    total_price = 0

    for cart_product in cart.cartproduct_set.all():
        total_price += cart_product.product.price * cart_product.quantity

    return total_price

def view_cart(request):
    # Attempt to get the user's cart or create a new one if it doesn't exist
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Calculate the total price of items in the cart
    total_price = calculate_cart_total(cart)

    # Retrieve the cart products, if the cart exists
    cart_products = cart.cartproduct_set.all()
    cart_item_count = cart.cartproduct_set.count()

    return render(request, 'cart.html', {'cart_item_count': cart_item_count, 'cart_products': cart_products, 'cart': cart, 'total_price': total_price})

def remove_from_cart(request, cart_product_id):
    cart_product = get_object_or_404(CartProduct, pk=cart_product_id)
    cart_product.delete()
    return redirect('view_cart')  # Redirect back to the cart page