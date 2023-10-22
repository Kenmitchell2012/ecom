from django.shortcuts import render, redirect
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
    cart_product, created = CartProduct.objects.get_or_create(cart=cart, product=product)
    cart_product.quantity += 1
    cart_product.save()
    return redirect('view_cart')

from django.shortcuts import render, get_object_or_404

def view_cart(request):
    # Attempt to get the user's cart or create a new one if it doesn't exist
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    
    # Retrieve the cart products, if the cart exists
    cart_products = cart.cartproduct_set.all()
    cart_item_count = cart.cartproduct_set.count()
    return render(request, 'cart.html', {'cart_item_count': cart_item_count, 'cart_products': cart_products, 'cart': cart})
