import csv
import datetime
from django.http import HttpResponse
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.urls import reverse
from .models import Order, OrderItem


def order_detail(obj):

    url = reverse('orders:admin_order_detail', args=[obj.id])
    return mark_safe(f'<a href="{url}">View</a>')


def order_pdf(obj):

    url = reverse('orders:admin_order_pdf', args=[obj.id])
    return mark_safe(f'<a href="{url}">PDF</a>')


order_pdf.short_description = 'Invoice'


def export_to_csv(modeladmin, request, queryset):
    """
    Create an instance of HTTPResponse specifying
    the text/csv content type and indicating
    with content_disposition header that
    it contains an attached file.
    Create a csv writer object that will
    write to the response object.

    Get model fields dynamically using get_fields()
    method of the model's _meta options, excluding
    many-to-many and one-to-many relationships.
    Write the row headers using field names
    and iterate over the given queryset to write
    a row for each object returned by the Queryset,
    making sure the datetime is formatted as a string
    as required by csv file.

    This generic administration action
    can be added to any ModelAdmin class.
    """
    opts = modeladmin.model._meta
    content_disposition = f'attachment; filename={opts.verbose_name}.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition
    writer = csv.writer(response)
    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]

    # write first row with header information
    writer.writerow([field.verbose_name for field in fields])

    # write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response


# customise the display name for the action
# in the drop-down element of the administration site
export_to_csv.short_description = 'Export to CSV'


def order_payment(obj):

    url = obj.get_stripe_url()
    if obj.stripe_id:
        html = f'<a href="{url}" target="_blank">{obj.stripe_id}</a>'
        return mark_safe(html)
    return ''


# customise the display name for the action
# in the element of the administration site
order_payment.short_description = 'Stripe payment'


class OrderItemInLine(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = ['id', 'first_name', 'last_name', 'email',
                    'address', 'postal_code', 'city', 'paid',
                    order_payment, 'created', 'updated', order_detail, order_pdf]
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInLine]

    # adding export_to_csv action to the OrderAdmin class
    actions = [export_to_csv]
