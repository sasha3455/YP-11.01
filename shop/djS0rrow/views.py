from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .models import Brand, Category, Clothes, Collection, Customer, Order, OrderItem, Review
from .forms import ClothesForm, LoginForm, RegisterForm


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(self.request, 'Недостаточно прав для выполнения действия.')
        return redirect('home')


def home_view(request):
    return render(request, 'home.html')


def info_view(request):
    return render(request, 'info.html')


def cart_view(request):
    cart = request.session.get('cart', {})
    clothes_ids = [int(item_id) for item_id in cart.keys()]
    clothes_map = Clothes.objects.in_bulk(clothes_ids)
    cart_items = []
    total = 0

    for item_id, quantity in cart.items():
        clothes = clothes_map.get(int(item_id))
        if not clothes:
            continue
        item_total = clothes.price * quantity
        total += item_total
        cart_items.append(
            {
                'clothes': clothes,
                'quantity': quantity,
                'item_total': item_total,
            }
        )

    return render(
        request,
        'cart.html',
        {
            'cart_items': cart_items,
            'total': total,
        },
    )


@require_POST
def add_to_cart_view(request, pk):
    clothes = get_object_or_404(Clothes, pk=pk, is_exists=True)
    cart = request.session.get('cart', {})
    item_id = str(clothes.pk)
    cart[item_id] = cart.get(item_id, 0) + 1
    request.session['cart'] = cart
    messages.success(request, f'Товар "{clothes.name}" добавлен в корзину.')
    return redirect(request.META.get('HTTP_REFERER', 'product_list'))


@require_POST
def remove_from_cart_view(request, pk):
    cart = request.session.get('cart', {})
    cart.pop(str(pk), None)
    request.session['cart'] = cart
    messages.success(request, 'Товар удален из корзины.')
    return redirect('cart_view')


@require_POST
def clear_cart_view(request):
    request.session['cart'] = {}
    messages.success(request, 'Корзина очищена.')
    return redirect('cart_view')


@login_required
@require_POST
@transaction.atomic
def create_order_from_cart_view(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, 'Корзина пуста.')
        return redirect('cart_view')

    customer, _ = Customer.objects.get_or_create(
        user=request.user,
        defaults={
            'first_name': request.user.first_name or request.user.username,
            'last_name': request.user.last_name or '-',
            'email': request.user.email or f'{request.user.username}@example.com',
            'phone': '',
        },
    )

    clothes_map = Clothes.objects.in_bulk([int(item_id) for item_id in cart.keys()])
    order = Order.objects.create(user=request.user, customer=customer, total_amount=0)
    total = 0

    for item_id, quantity in cart.items():
        clothes = clothes_map.get(int(item_id))
        if not clothes:
            continue
        item_total = clothes.price * quantity
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
    request.session['cart'] = {}
    messages.success(request, f'Заказ №{order.pk} успешно создан.')
    return redirect('order_detail', pk=order.pk)


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'Регистрация прошла успешно.')
        return redirect('home')
    return render(request, 'auth/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        messages.success(request, 'Вы успешно вошли в аккаунт.')
        return redirect('home')
    return render(request, 'auth/login.html', {'form': form})


@login_required
@require_POST
def logout_view(request):
    logout(request)
    messages.success(request, 'Вы вышли из аккаунта.')
    return redirect('home')


class ClothesListView(ListView):
    model = Clothes
    template_name = 'clothes/clothes_list.html'
    context_object_name = 'clothes'
    queryset = Clothes.objects.select_related('category', 'brand').filter(is_exists=True)


class ClothesDetailView(DetailView):
    model = Clothes
    template_name = 'clothes/clothes_detail.html'
    context_object_name = 'clothes'


class ClothesCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Clothes
    form_class = ClothesForm
    template_name = 'clothes/clothes_form.html'
    success_url = reverse_lazy('product_list')


class ClothesUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Clothes
    form_class = ClothesForm
    template_name = 'clothes/clothes_form.html'

    def get_success_url(self):
        return reverse_lazy('product_detail', kwargs={'pk': self.object.pk})


class ClothesDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Clothes
    template_name = 'clothes/clothes_confirm_delete.html'
    success_url = reverse_lazy('product_list')


class CategoryListView(ListView):
    model = Category
    template_name = 'category/category_list.html'
    context_object_name = 'categories'


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'category/category_detail.html'
    context_object_name = 'category'


class CategoryCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Category
    fields = ['name', 'description']
    template_name = 'category/category_form.html'
    success_url = reverse_lazy('category_list')


class CategoryUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Category
    fields = ['name', 'description']
    template_name = 'category/category_form.html'

    def get_success_url(self):
        return reverse_lazy('category_detail', kwargs={'pk': self.object.pk})


class CategoryDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Category
    template_name = 'category/category_confirm_delete.html'
    success_url = reverse_lazy('category_list')


class CollectionListView(ListView):
    model = Collection
    template_name = 'collection/collection_list.html'
    context_object_name = 'collections'


class CollectionDetailView(DetailView):
    model = Collection
    template_name = 'collection/collection_detail.html'
    context_object_name = 'collection'


class CollectionCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Collection
    fields = ['name', 'description', 'season']
    template_name = 'collection/collection_form.html'
    success_url = reverse_lazy('collection_list')


class CollectionUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Collection
    fields = ['name', 'description', 'season']
    template_name = 'collection/collection_form.html'

    def get_success_url(self):
        return reverse_lazy('collection_detail', kwargs={'pk': self.object.pk})


class CollectionDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Collection
    template_name = 'collection/collection_confirm_delete.html'
    success_url = reverse_lazy('collection_list')


class BrandListView(ListView):
    model = Brand
    template_name = 'brand/brand_list.html'
    context_object_name = 'brands'


class BrandDetailView(DetailView):
    model = Brand
    template_name = 'brand/brand_detail.html'
    context_object_name = 'brand'


class BrandCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Brand
    fields = ['name', 'description', 'country', 'logo']
    template_name = 'brand/brand_form.html'
    success_url = reverse_lazy('brand_list')


class BrandUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Brand
    fields = ['name', 'description', 'country', 'logo']
    template_name = 'brand/brand_form.html'

    def get_success_url(self):
        return reverse_lazy('brand_detail', kwargs={'pk': self.object.pk})


class BrandDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Brand
    template_name = 'brand/brand_confirm_delete.html'
    success_url = reverse_lazy('brand_list')


class CustomerListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = Customer
    template_name = 'customer/customer_list.html'
    context_object_name = 'customers'


class CustomerDetailView(LoginRequiredMixin, StaffRequiredMixin, DetailView):
    model = Customer
    template_name = 'customer/customer_detail.html'
    context_object_name = 'customer'


class CustomerCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Customer
    fields = ['first_name', 'last_name', 'email', 'phone']
    template_name = 'customer/customer_form.html'
    success_url = reverse_lazy('customer_list')


class CustomerUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Customer
    fields = ['first_name', 'last_name', 'email', 'phone']
    template_name = 'customer/customer_form.html'

    def get_success_url(self):
        return reverse_lazy('customer_detail', kwargs={'pk': self.object.pk})


class CustomerDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Customer
    template_name = 'customer/customer_confirm_delete.html'
    success_url = reverse_lazy('customer_list')


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'order/order_list.html'
    context_object_name = 'orders'
    queryset = Order.objects.select_related('customer', 'user')

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(user=self.request.user)


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'order/order_detail.html'
    context_object_name = 'order'


    def get_queryset(self):
        queryset = super().get_queryset().select_related('customer', 'user')
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(user=self.request.user)


class OrderCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Order
    fields = ['customer', 'status', 'total_amount']
    template_name = 'order/order_form.html'
    success_url = reverse_lazy('order_list')


class OrderUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Order
    fields = ['customer', 'status', 'total_amount']
    template_name = 'order/order_form.html'

    def get_success_url(self):
        return reverse_lazy('order_detail', kwargs={'pk': self.object.pk})


class OrderDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Order
    template_name = 'order/order_confirm_delete.html'
    success_url = reverse_lazy('order_list')


class OrderItemListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = OrderItem
    template_name = 'orderitem/orderitem_list.html'
    context_object_name = 'order_items'
    queryset = OrderItem.objects.select_related('order', 'clothes', 'order__customer')


class OrderItemDetailView(LoginRequiredMixin, StaffRequiredMixin, DetailView):
    model = OrderItem
    template_name = 'orderitem/orderitem_detail.html'
    context_object_name = 'order_item'


class OrderItemCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = OrderItem
    fields = ['order', 'clothes', 'quantity', 'price_at_order']
    template_name = 'orderitem/orderitem_form.html'
    success_url = reverse_lazy('order_item_list')


class OrderItemUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = OrderItem
    fields = ['order', 'clothes', 'quantity', 'price_at_order']
    template_name = 'orderitem/orderitem_form.html'

    def get_success_url(self):
        return reverse_lazy('order_item_detail', kwargs={'pk': self.object.pk})


class OrderItemDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = OrderItem
    template_name = 'orderitem/orderitem_confirm_delete.html'
    success_url = reverse_lazy('order_item_list')


class ReviewListView(ListView):
    model = Review
    template_name = 'review/review_list.html'
    context_object_name = 'reviews'
    queryset = Review.objects.select_related('clothes', 'customer')


class ReviewDetailView(DetailView):
    model = Review
    template_name = 'review/review_detail.html'
    context_object_name = 'review'


class ReviewCreateView(CreateView):
    model = Review
    fields = ['clothes', 'customer', 'rating', 'text']
    template_name = 'review/review_form.html'
    success_url = reverse_lazy('review_list')


class ReviewUpdateView(UpdateView):
    model = Review
    fields = ['clothes', 'customer', 'rating', 'text']
    template_name = 'review/review_form.html'

    def get_success_url(self):
        return reverse_lazy('review_detail', kwargs={'pk': self.object.pk})


class ReviewDeleteView(DeleteView):
    model = Review
    template_name = 'review/review_confirm_delete.html'
    success_url = reverse_lazy('review_list')
