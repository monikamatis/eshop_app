from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    """
    Use this form to add items to the cart.

    quantity - allows user to select quantity
        from 1 to 20,coerce=int parameter converts input to int.
    override - allows to select if the quantity is to be
        added (default - False) to the current quantity
        in the cart or if it should override the existing
        quantity (default True).
    """
    quantity = forms.TypedChoiceField(
                                choices=PRODUCT_QUANTITY_CHOICES,
                                coerce=int)

    override = forms.BooleanField(required=False,
                                  initial=False,
                                  widget=forms.HiddenInput)


