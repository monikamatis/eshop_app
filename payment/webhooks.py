import stripe
from stripe import error
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from orders.models import Order


@csrf_exempt
def stripe_webhook(request):
    """
    Using stripe.Webhook.construct_event method to verify
    the event's signature header. csrf_exempt decorator is used
    to prevent Django's validator from performing CSRF validation
    which is done by default for ALL POST requests.
    :param request: takes request
    :return: return HttpResponse
    """
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET)

    except ValueError as e:

        # invalid payload
        return HttpResponse(status=400)

    except stripe.error.SignatureVerificationError as e:

        # invalid signature
        return HttpResponse(status=400)

    if event.type == 'checkout.session.completed':
        session = event.data.object
        if session.mode == 'payment' and session.payment_status == 'paid':
            try:
                order = Order.objects.get(id=session.client_reference_id)

            except Order.DoesNotExist:
                return HttpResponse(status=404)
            # mark order as paid
            order.paid = True
            # store Stripe payment ID
            order.stripe_id = session.payment_intent
            order.save()

    return HttpResponse(status=200)
