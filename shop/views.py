from django.shortcuts import render, get_object_or_404
from .models import Category, Product

# adds Add to Cart button logic to product_detail view
from cart.forms import CartAddProductForm


def product_list(request, category_slug=None):
    """
    Define a product list view for the product catalog.
    :param request: required parameter of a function defining a view
    :param category_slug: defaults to None
    :return: a list of all available products with relevant categories
        or 'not found' error page.
    """
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if category_slug:

        category = get_object_or_404(Category,
                                     slug=category_slug)
        products = products.filter(category=category)

    return render(request, 'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})


# may need to change a parameter in product_detail function if
# it causes problems ('shadows built-in name')
def product_detail(request, id, slug):
    """
    Define a detailed product view.
    :param request: required parameter for any view function
    :param id: product id
    :param slug: product slug; its inclusion allows for SEO-friendly URLs
    :return: details of a product with add to cart form
        or 'not found' error page.
    """
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'shop/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form})
