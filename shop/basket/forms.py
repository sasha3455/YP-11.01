from django import forms


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, max_value=100, initial=1, label='Количество')
    override_quantity = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput,
    )


class OrderCreateForm(forms.Form):
    confirm = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.HiddenInput,
    )

