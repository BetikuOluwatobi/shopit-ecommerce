from django.shortcuts import render,reverse,redirect
from cart.carts import Cart
from .models import OrderItem,Order
from .forms import OrderForm
from .task import order_created
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint

# Create your views here.
@staff_member_required
def admin_order_pdf(request,order_id):
  order = get_object_or_404(Order,id=order_id)
  html = render_to_string('orders\order\pdf.html',{'order':order})
  response = HttpResponse(content_type='application/pdf')
  response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
  weasyprint.HTML(string=html).write_pdf(response,stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')])
  return response

@staff_member_required
def admin_order_detail(request,order_id):
  order = get_object_or_404(Order,id=order_id)
  return render(request,'admin/orders/order/detail.html',{'order':order})

def order_create(request):
  cart = Cart(request)
  if request.method == 'POST':
    order_form = OrderForm(request.POST)
    if order_form.is_valid():
      order = order_form.save()
      for item in cart:
        OrderItem.objects.create(order=order,product=item['product'],
        price=item['price'],quantity=item['quantity'])
        # clear cart
      cart.clear()
      order_created.delay(order.id)
      request.session['order_id'] = order.id
      return redirect(reverse('payment:process'))
  else:
    order_form = OrderForm()
    return render(request,'orders/order/create.html',{'order_form':order_form,'cart':cart})
