from celery import shared_task
from django.core.mail import send_mail

from .models import Order


@shared_task
def order_created(order_id, total):
    """
    Task to send an e-mail notification when an order is successfully created.
    :param order_id: id field of Order
    :return: send an email notification about a successful order.
    """
    order = Order.objects.get(id=order_id)
    subject = f'Order number: {order_id}'
    message = f'Dear {order.first_name}, \n\n' \
              f'You have successfully placed an order.' \
              f'Your order ID is {order_id}.' \
              f'Your order total is {total} USD.'
    mail_sent = send_mail(subject,
                          message,
                          'admin@e_commerce_basic.com',
                          [order.email])

    return mail_sent
