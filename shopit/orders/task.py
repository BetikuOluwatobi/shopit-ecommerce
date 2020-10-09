from celery import task
from django.core.mail import send_mail
from .models import Order

@task
def order_created(order_id):
  """
  Task to send an email successfully when an order is placed
  """

  order = Order(id=order_id)
  subject = f'Order nr:{order.id}'
  message = f'Dear {order.name}, \n\n' \
            f'You have successfully placed an order.' \
            f'You order ID is {order.id}'
  mail_sent = send_mail(subject,message,'admin@shopit.com',[order.email])

  return mail_sent