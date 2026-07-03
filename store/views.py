from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Product, Category, Cart, Order, OrderItem


def home(request):

    query = request.GET.get('q')

    categories = Category.objects.all()

    products = Product.objects.filter(available=True)

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(brand__icontains=query) |
            Q(description__icontains=query)
        )

    products = products.order_by('-created_at')

    return render(
        request,
        'home.html',
        {
            'products': products,
            'categories': categories,
            'query': query
        }
    )


def category_products(request, category_id):

    categories = Category.objects.all()

    selected_category = get_object_or_404(
        Category,
        id=category_id
    )

    products = Product.objects.filter(
        category=selected_category,
        available=True
    ).order_by('-created_at')

    return render(
        request,
        'home.html',
        {
            'products': products,
            'categories': categories,
            'selected_category': selected_category
        }
    )


def product_detail(request, id):

    product = get_object_or_404(
        Product,
        id=id,
        available=True
    )

    return render(
        request,
        'product_detail.html',
        {
            'product': product
        }
    )


@login_required(login_url='login')
def add_to_cart(request, id):

    product = get_object_or_404(Product, id=id)

    if product.stock <= 0:
        return redirect('home')

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:

        if cart_item.quantity < product.stock:
            cart_item.quantity += 1
            cart_item.save()

    return redirect('cart')


@login_required(login_url='login')
def cart(request):

    cart_items = Cart.objects.filter(
        user=request.user
    )

    total = sum(
        item.total_price()
        for item in cart_items
    )

    return render(
        request,
        'cart.html',
        {
            'cart_items': cart_items,
            'total': total
        }
    )


@login_required(login_url='login')
def increase_quantity(request, item_id):

    item = get_object_or_404(
        Cart,
        id=item_id,
        user=request.user
    )

    if item.quantity < item.product.stock:
        item.quantity += 1
        item.save()

    return redirect('cart')


@login_required(login_url='login')
def decrease_quantity(request, item_id):

    item = get_object_or_404(
        Cart,
        id=item_id,
        user=request.user
    )

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect('cart')


@login_required(login_url='login')
def remove_from_cart(request, item_id):

    item = get_object_or_404(
        Cart,
        id=item_id,
        user=request.user
    )

    item.delete()

    return redirect('cart')


@login_required(login_url='login')
def checkout(request):

    cart_items = Cart.objects.filter(
        user=request.user
    )

    if not cart_items.exists():
        return redirect('cart')

    total = sum(
        item.total_price()
        for item in cart_items
    )

    order = Order.objects.create(
        user=request.user,
        total_amount=total
    )

    for item in cart_items:

        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )

        item.product.stock -= item.quantity
        item.product.save()

    cart_items.delete()

    return render(
        request,
        'checkout_success.html',
        {
            'order': order,
            'total': total
        }
    )


@login_required(login_url='login')
def orders(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(
        request,
        'orders.html',
        {
            'orders': orders
        }
    )