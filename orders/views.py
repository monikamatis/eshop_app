from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created
import weasyprint


@staff_member_required
def admin_order_pdf(request, order_id):

    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html',
                            {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    weasyprint.HTML(string=html).write_pdf(response,
                                           stylesheets=[weasyprint.CSS(settings.STATIC_ROOT / 'css/pdf.css')])

    return response


def order_create(request):
    """

    :param request:
    :return:
    """
    cart = Cart(request)
    total = 0
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
                total += int(item['price']) * int(item['quantity'])
            # clear the cart
            cart.clear()

            # launching asynchronous task - send an email notification
            order_created.delay(order.id, total)
            # set up the order in the session
            request.session['order_id'] = order.id
            # redirect for payment
            return redirect(reverse('payment:process'))

    else:
        form = OrderCreateForm()

    return render(request,
                  'orders/order/create.html',
                  {'cart': cart, 'form': form})


@staff_member_required
def admin_order_detail(request, order_id):
    """
    Get the Order object with given ID and
    display details of the order in the customised template.

    The staff_member_required decorator ensures that both is_active
    and is_staff fields of the user requesting the page are set to TRUE.

    :param request: required parameter of any view function
    :param order_id: id field of the Order model
    :return:  render a detailed admin page for the given order.
    """
    order = get_object_or_404(Order, id=order_id)
    return render(request,
                  'admin/orders/order/detail.html',
                  {'order': order})
