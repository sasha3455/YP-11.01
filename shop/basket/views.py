from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from djS0rrow.models import Clothes, Customer, Order, OrderItem

from .basket import Basket
from .forms import CartAddProductForm, OrderCreateForm


def basket_detail_view(request):
    basket = Basket(request)
    basket_items = []
    for item in basket:
        item['update_quantity_form'] = CartAddProductForm(
            initial={'quantity': item['quantity'], 'override_quantity': True}
        )
        basket_items.append(item)
    return render(
        request,
        'basket/detail.html',
        {
            'cart_items': basket_items,
            'total': basket.get_total_price(),
        },
    )


@require_POST
def basket_add_view(request, pk):
    clothes = get_object_or_404(Clothes, pk=pk, is_exists=True)
    basket = Basket(request)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        basket.add(
            clothes=clothes,
            quantity=form.cleaned_data['quantity'],
            override_quantity=form.cleaned_data['override_quantity'],
        )
    else:
        basket.add(clothes=clothes, quantity=1)
    messages.success(request, f'Товар "{clothes.name}" добавлен в корзину.')
    return redirect(request.META.get('HTTP_REFERER', 'product_list'))


@require_POST
def basket_update_view(request, pk):
    clothes = get_object_or_404(Clothes, pk=pk, is_exists=True)
    basket = Basket(request)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        basket.add(
            clothes=clothes,
            quantity=form.cleaned_data['quantity'],
            override_quantity=True,
        )
        messages.success(request, 'Количество товара в корзине обновлено.')
    return redirect('cart_view')


@require_POST
def basket_remove_view(request, pk):
    clothes = get_object_or_404(Clothes, pk=pk)
    basket = Basket(request)
    basket.remove(clothes)
    messages.success(request, 'Товар удален из корзины.')
    return redirect('cart_view')


@require_POST
def basket_clear_view(request):
    Basket(request).clear()
    messages.success(request, 'Корзина очищена.')
    return redirect('cart_view')


@login_required
def order_create_view(request):
    basket = Basket(request)
    if len(basket) == 0:
        messages.error(request, 'Корзина пуста.')
        return redirect('cart_view')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            return _create_order(request, basket)
    else:
        form = OrderCreateForm()

    return render(
        request,
        'basket/order/order_form.html',
        {
            'form': form,
            'cart_items': list(basket),
            'total': basket.get_total_price(),
        },
    )


@transaction.atomic
def _create_order(request, basket):
    customer, _ = Customer.objects.get_or_create(
        user=request.user,
        defaults={
            'first_name': request.user.first_name or request.user.username,
            'last_name': request.user.last_name or '-',
            'email': request.user.email or f'{request.user.username}@example.com',
            'phone': '',
        },
    )

    order = Order.objects.create(user=request.user, customer=customer, total_amount=0)
    total = 0

    for item in basket:
        clothes = item['clothes']
        quantity = item['quantity']
        item_total = item['item_total']
        total += item_total
        OrderItem.objects.create(
            order=order,
            clothes=clothes,
            quantity=quantity,
            price_at_order=clothes.price,
        )

    if total == 0:
        order.delete()
        messages.error(request, 'Не удалось создать заказ из корзины.')
        return redirect('cart_view')

    order.total_amount = total
    order.save(update_fields=['total_amount'])
    basket.clear()
    messages.success(request, f'Заказ №{order.pk} успешно создан.')
    return redirect('order_detail', pk=order.pk)

