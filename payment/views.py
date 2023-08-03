from decimal import Decimal
import stripe
from django.conf import settings
from django.shortcuts import render, redirect, reverse, get_object_or_404
from orders.models import Order


# create the Stripe instance
stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION


def payment_process(request):
    """
    Display the order summary to the user,
    creates the Stripe checkout session
    and redirects the user to the Stripe-hosted payment form.
    :param request: required parameter in a view function
    :return: render payment/process.html
    """
    order_id = request.session.get('order_id', None)
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        success_url = request.build_absolute_uri(reverse('payment:completed'))
        cancel_url = request.build_absolute_uri(reverse('payment:canceled'))

        # Stripe checkout session data
        # https://stripe.com/docs/api/checkout/sessions/object#checkout_session_object-mode
        session_data = {
            'mode': 'payment',
            'client_reference_id': order.id,
            'success_url': success_url,
            'cancel_url': cancel_url,
            'line_items': []
        }

        # add order items to the Stripe checkout session
        for item in order.items.all():
            session_data['line_items'].append({
                'price_data': {
                    # the amount in the smallest currency unit with no decimal places to be collected
                    'unit_amount': int(item.price * Decimal('100')),
                    # currency to use in three-letter ISO format
                    # see supported currencies at https://stripe.com/docs/currencies
                    'currency': 'usd',
                    'product_data': {
                        'name': item.product.name,
                    },
                },
                'quantity': item.quantity,
            })

        # create Stripe checkout session
        session = stripe.checkout.Session.create(**session_data)
        # redirect to Stripe payment form
        return redirect(session.url, code=303)

    else:
        return render(request, 'payment/process.html', locals())


def payment_completed(request):
    """
    Display the page to which Stripe directs
    the user when the payment is successful.
    :param request: required parameter in a view function
    :return: render payment/completed.html
    """
    return render(request, 'payment/completed.html')


def payment_canceled(request):
    """
    Display the page to which Stripe directs
    the user when the payment is canceled/unsuccessful.
    :param request: required parameter in a view function
    :return: render payment/canceled.html
    """
    return render(request, 'payment/canceled.html')
