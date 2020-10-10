from io import BytesIO
from celery import task
from orders.models import Order
from django.conf import settings
import weasyprint
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

@task
def payment_completed(order_id):
  '''
  Task to send email after successful completion of orders.
  '''
  order = Order.objects.get(id=order_id)
  html = render_to_string('orders/order/pdf.html',{'order':order})
  subject = f'My Shop - EE Invoice no. {order.id}'
  message = f"Please, find attached to this mail your purchase Invoice"
  email = EmailMessage(subject,message,'admin@myshop',[order.email])
  stylesheet = [weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')]
  out = BytesIO()
  weasyprint.HTML(string=html).write_pdf(out,stylesheet)
  email.attach(f'order_{order.id}.pdf',out.getvalue(),'application/pdf')
  email.send()