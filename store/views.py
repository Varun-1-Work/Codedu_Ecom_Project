from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from decimal import Decimal
from .models import Category, Product


# -----------------------------
# HOME PAGE
# -----------------------------
def index(request):
    return render(request, 'index.html')


# -----------------------------
# COLLECTIONS PAGE
# -----------------------------
@login_required(login_url='login')
def collections(request):
    products = Product.objects.filter(status=0)
    return render(request, 'collections.html', {"products": products})


# -----------------------------
# LOGIN
# -----------------------------
def loginn(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid login')
            return redirect('login')

    return render(request, 'login.html')


# -----------------------------
# REGISTER
# -----------------------------
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.info(request, "Username already exists")
            return redirect('register')

        elif User.objects.filter(email=email).exists():
            messages.info(request, "Email already Taken")
            return redirect('register')

        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            return redirect('/')

    return render(request, 'register.html')


# -----------------------------
# OTHER STATIC PAGES
# -----------------------------
def blog_list(request):
    return render(request, 'blog_list.html')


def about(request):
    return render(request, 'about.html')


def testimonial(request):
    return render(request, 'testimonial.html')


def product(request):
    products = Product.objects.filter(status=0)
    return render(request, 'product.html', {"products": products})


def contact(request):
    return render(request, 'contact.html')


# -----------------------------
# SESSION CART UTILITIES
# -----------------------------
def _get_cart(session):
    return session.get('cart', {})


def _save_cart(session, cart):
    session['cart'] = cart
    session.modified = True


# -----------------------------
# ADD TO CART
# -----------------------------
@require_POST
def add_to_cart(request, product_id):

    product = get_object_or_404(Product, id=product_id)
    cart = _get_cart(request.session)

    # quantity
    try:
        qty = int(request.POST.get('quantity', 1))
    except:
        qty = 1

    if qty < 1:
        qty = 1

    pid = str(product_id)

    # safe image
    image_url = product.product_image.url if product.product_image else ''

    # add/update
    if pid in cart:
        cart[pid]['quantity'] += qty
    else:
        cart[pid] = {
            'title': product.name,
            'price': str(product.selling_price),
            'quantity': qty,
            'image': image_url,
        }

    _save_cart(request.session, cart)
    messages.success(request, f"{product.name} added to cart.")
    return redirect('cart_detail')


# -----------------------------
# CART DETAIL
# -----------------------------
def cart_detail(request):
    cart = _get_cart(request.session)
    items = []
    total = Decimal('0.00')

    for pid, data in cart.items():
        price = Decimal(data.get('price', '0'))
        quantity = data.get('quantity', 0)
        subtotal = price * quantity
        total += subtotal

        items.append({
            'product_id': pid,
            'title': data.get('title', ''),
            'price': price,
            'quantity': quantity,
            'subtotal': subtotal,
            'image': data.get('image', ''),
        })

    return render(request, 'cart.html', {
        'cart_items': items,
        'cart_total': total,
    })


# -----------------------------
# UPDATE CART
# -----------------------------
@require_POST
def update_cart(request, product_id):
    cart = _get_cart(request.session)
    pid = str(product_id)

    if pid in cart:
        try:
            quantity = int(request.POST.get('quantity', 1))
        except:
            quantity = 1

        if quantity <= 0:
            cart.pop(pid)
        else:
            cart[pid]['quantity'] = quantity

        _save_cart(request.session, cart)

    return redirect('cart_detail')


# -----------------------------
# REMOVE ITEM
# -----------------------------
def remove_from_cart(request, product_id):
    cart = _get_cart(request.session)
    pid = str(product_id)

    if pid in cart:
        cart.pop(pid)
        _save_cart(request.session, cart)

    return redirect('cart_detail')


# -----------------------------
# DEBUG CART PAGE
# -----------------------------
def debug_cart(request):
    cart = request.session.get('cart', {})
    return render(request, 'debug_cart.html', {
        'raw_cart': cart,
        'session_keys': list(request.session.keys())
    })


# -----------------------------
# LOGOUT
# -----------------------------
def logout(request):
    auth.logout(request)
    return redirect('/')
