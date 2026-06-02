from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Clothes, Customer


class ClothesForm(forms.ModelForm):
    class Meta:
        model = Clothes
        fields = [
            'name',
            'description',
            'price',
            'size',
            'color',
            'photo',
            'is_exists',
            'category',
            'brand',
        ]


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')
    first_name = forms.CharField(required=True, label='Имя')
    last_name = forms.CharField(required=True, label='Фамилия')
    phone = forms.CharField(required=False, label='Телефон')

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
            Customer.objects.get_or_create(
                user=user,
                defaults={
                    'first_name': self.cleaned_data['first_name'],
                    'last_name': self.cleaned_data['last_name'],
                    'email': self.cleaned_data['email'],
                    'phone': self.cleaned_data.get('phone', ''),
                },
            )
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, max_value=100, initial=1, label='Количество')
    override_quantity = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput,
    )
