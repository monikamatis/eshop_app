from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm


# @require_POST decorator - used to allow ONLY POST requests.
@require_POST
def cart_add(request, product_id):
    """
    Receive product ID as a parameter and
    retrieve the Product instance with given ID;
    Validate CartAddProductForm - if valid,
    add or update item in the cart and redirect
    to the cart_detail URL to display cart contents.
    :param request: required parameter for any view
    :param product_id: passing product id value
    :return: redirect to the cart_detail page.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 override_quantity=cd['override'])

    return redirect('cart:cart_detail')


# @require_POST decorator - used to allow ONLY POST requests.
@require_POST
def cart_remove(request, product_id):
    """
    Receive product ID as a parameter and
    retrieve the Product instance with given ID;
    Remove the item from the cart and redirect
    to the cart_detail URL to display cart contents.
    :param request: required parameter for any view
    :param product_id: passing product id value
    :return: redirect to the cart_detail page.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    """
    Get the current cart and display it
    :param request: required parameter for any view
    :return: redirect to the cart_detail page.
    """
    cart = Cart(request)

    # form for updating quantity in the cart
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
                            'quantity': item['quantity'],
                            'override': True})

    return render(request, 'cart/detail.html', {'cart': cart})
