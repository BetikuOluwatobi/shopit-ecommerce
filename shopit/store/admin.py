from django.contrib import admin
from store.models import Category,Product

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
  list_display = ['name','slug']
  prepopulated_fields = {'slug':('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
  list_display = ['name','category','available','price','created','updated']
  list_filter = ['category','price','created','updated']
  list_editable = ['price','available']
  prepopulated_fields = {'slug':('name',)}