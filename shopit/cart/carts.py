from decimal import Decimal
from django.conf import settings
from store.models import Product
from django.urls import reverse_lazy

class Cart(object):

  def __init__(self,request):
    """
    Initialize the cart.
    """
    #assign session to object instance
    self.session = request.session
    #get cart_session_id if any
    cart = self.session.get(settings.CART_SESSION_ID)
    #if no cart session with user
    if not cart:
      #assign a new cart session to user
      cart = self.session[settings.CART_SESSION_ID] = {}
    self.cart = cart
  
  def add(self,product,quantity=1,overide_quantity=False):
    """
    Add to Carts
    """
    product_id = str(product.id)
    # Check if product in cart already
    if product_id not in self.cart:
      # assigns a new product to class
      self.cart[product_id] = {'quantity':0,'price':str(product.price)}
    #overide current quantity of product
    if overide_quantity:
      self.cart[product_id]['quantity'] = quantity
    #Update current products quantity
    else:
      self.cart[product_id]['quantity'] += quantity
    self.save()

  def save(self):
     #mark the session as "modified" to make sure it gets saved
    self.session.modified = True

  def remove(self,product):
    #get product's id
    product_id = str(product.id)
    if product_id in self.cart:
      del self.cart[product_id]
      self.save()

  def __iter__(self):
    '''
    Iterate over the items in the cart and get the products
    from the database.
    '''
    product_ids = self.cart.keys()
    products = Product.objects.filter(id__in=product_ids)

    cart = self.cart.copy()
    for product in products:
      cart[str(product.id)]['product'] = product

    for item in cart.values():
      item['price'] = Decimal(item['price'])
      item['total_price'] = item['price'] * item['quantity']
      yield item

  def __len__(self):
    '''
    Count all items in the Cart
    '''
    return sum(item['quantity'] for item in self.cart.values())
  
  def get_total_price(self):
    '''
    Sum Total Price
    '''
    return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
  
  def clear(self):
    '''
    Clear Session
    '''
    del self.session[settings.CART_SESSION_ID]
    self.save()

  def get_absolute_url(self):
    return reverse_lazy('cart:cart_detail')