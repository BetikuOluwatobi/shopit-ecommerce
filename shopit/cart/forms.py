from django import forms

PRODUCT_QUANTITY_CHOICES = [(i,str(i)) for i in range(1,101)]

class CartAddProductForms(forms.Form):
  quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES,coerce=int,)
  override = forms.BooleanField(required=False,widget=forms.HiddenInput,initial=False)
