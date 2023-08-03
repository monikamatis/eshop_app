from .cart import Cart


def cart(request):
    """
    Set the current cart into a request context.
    :param request: request object
    :return: Instantiates the cart with a request object
        and make it available to all templates as a variable named 'cart'.
    """
    return {'cart': Cart(request)}
