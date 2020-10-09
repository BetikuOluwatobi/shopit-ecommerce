from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
  name = models.CharField(max_length=200,db_index=True)
  slug = models.SlugField(max_length=200,unique=True)

  class Meta:
    ordering = ('name',)
    verbose_name = 'category'
    verbose_name_plural = 'categories'
  
  def get_absolute_url(self):
    return reverse('store:product_by_category_list',args=[self.slug,])

  def __str__(self):
    return self.name

class Product(models.Model):
  category = models.ForeignKey(Category,related_name='products',on_delete=models.CASCADE)
  name = models.CharField(max_length=200,db_index=True)
  slug = models.SlugField(max_length=200,db_index=True)
  description = models.TextField(blank=True)
  image = models.ImageField(upload_to='products/%Y/%m/%d',blank=True)
  # Not it is better to use decimal fields to float fields when storing monetary
  # values in order to avoid rounding issues
  price = models.DecimalField(max_digits=10,decimal_places=2)
  available = models.BooleanField(default=True)
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)

  def get_absolute_url(self):
    return reverse('store:product_detail',args=[self.id,self.slug])
  class Meta:
    ordering = ('name',)
    index_together = (('id','slug'),)

  def __str__(self):
    return self.name

