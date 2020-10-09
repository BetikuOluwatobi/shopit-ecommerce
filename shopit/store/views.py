from django.shortcuts import render,redirect,reverse,get_object_or_404
from django.views import View,generic
from .models import Category,Product
from cart.forms import CartAddProductForms

# Create your views here.
def product_list(request,category_slug=None):
  category = None
  categories = Category.objects.all()
  products = Product.objects.filter(available=True)
  if category_slug:
    category = get_object_or_404(Category,slug=category_slug)
    products = Product.objects.filter(category=category)
  ctx = {'category':category,'products':products,'category_list':categories}
  return render(request,'store/product/list.html',ctx)

def product_detail(request,id,slug):
  product = get_object_or_404(Product,id=id,slug=slug,available=True)
  cart_product_form = CartAddProductForms()
  return render(request,'store/product/detail.html',{'product':product,'cart_product_form':cart_product_form})