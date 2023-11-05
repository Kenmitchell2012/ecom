from django.shortcuts import render

# Create your views here.

def cart_summary(request):
    username = request.user.username
    return render(request, 'cart_summary.html', {'username': username})

def cart_add(request):
    pass

def cart_delete(request):
    pass

def cart_update(request):
    pass
