from django.shortcuts import render,redirect,get_object_or_404
from django.conf import settings
from orders.models import Order
import braintree

# Create your views here.
gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)

def payment_process(request):
  order_id = request.session.get('order_id')
  order = get_object_or_404(Order,id=order_id)
  total_cost = order.get_total_price()
  if request.method == 'POST':
    nonce = request.POST.get('payment_method_nonce',None)
    results = gateway.transaction.sale({
      'amount':f'{total_cost:.2f}',
      'payment_method_nonce':nonce,
      'options':{
        'submit_for_settlement':True
        }
    })
    if results.is_success:
      order.paid = True
      order.braintree_id = results.transaction.id
      order.save()
      return redirect('payment:done')
    else:
      return redirect('payment:canceled')
  else:
    client_token = gateway.client_token.generate()
    return render(request,'payments/process.html',{'order':order,'client_token':client_token})


def payment_done(request):
  return render(request,'payments/done.html')

def payment_canceled(request):
  return render(request,'payments/canceled.html')