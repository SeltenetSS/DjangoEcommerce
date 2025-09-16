# from django.shortcuts import render, get_object_or_404, redirect
# from .models import Product
# from django.http import HttpResponseRedirect
# from django.urls import reverse
#
#
# def home(request):
#     products = Product.objects.all()
#     return render(request, 'home.html', {'products': products})
#
#
# def product_detail(request, slug):
#     product = get_object_or_404(Product, slug=slug)
#     return render(request, 'product_detail.html', {'product': product})
#
#
# def add_product(request):
#     if request.method == 'POST':
#         name = request.POST['name']
#         price = request.POST['price']
#         quantity = request.POST['quantity']
#         image_url = request.POST['image_url']
#         Product.objects.create(name=name, price=price, quantity=quantity, image_url=image_url)
#         return redirect('home')
#     return render(request, 'add_product.html')
#
#
# def add_to_cart(request, product_id):
#     cart = request.session.get('cart', {})
#     cart[product_id] = cart.get(product_id, 0) + 1
#     request.session['cart'] = cart
#     return HttpResponseRedirect(reverse('cart'))
#
# def cart_view(request):
#     cart = request.session.get('cart', {})
#     cart_items = []
#     total = 0
#
#     for product_id, qty in cart.items():
#         product = Product.objects.get(id=product_id)
#         subtotal = product.price * qty
#         total += subtotal
#         cart_items.append({
#             'product': product,
#             'qty': qty,
#             'subtotal': subtotal
#         })
#
#     return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})
#


from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages


def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'product_detail.html', {'product': product})


def add_product(request):
    if request.method == 'POST':
        name = request.POST['name']
        price = request.POST['price']
        quantity = request.POST['quantity']
        image_url = request.POST['image_url']
        Product.objects.create(name=name, price=price, quantity=quantity, image_url=image_url)
        return redirect('home')
    return render(request, 'add_product.html')


# Səbətə əlavə etmək
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if product.quantity <= 0:
        messages.error(request, 'This product is out of stock.')
        return redirect('home')

    cart = request.session.get('cart', {})

    # Əgər məhsul artıq səbətdə varsa, quantity-ni artır
    cart[product_id] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart

    # Məhsul stokunu azaldırıq
    product.quantity -= 1
    product.save()

    return HttpResponseRedirect(reverse('cart'))


# Səbəti göstərmək
def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for product_id, qty in cart.items():
        product = Product.objects.get(id=product_id)
        subtotal = product.price * qty
        total += subtotal
        cart_items.append({
            'product': product,
            'qty': qty,
            'subtotal': subtotal
        })

    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})



def update_cart(request, product_id, action):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        if action == 'increase' and product.quantity > 0:
            cart[str(product_id)] += 1
            product.quantity -= 1
            product.save()
        elif action == 'decrease':
            cart[str(product_id)] -= 1
            product.quantity += 1
            product.save()
            if cart[str(product_id)] <= 0:
                del cart[str(product_id)]

    request.session['cart'] = cart
    return redirect('cart')
