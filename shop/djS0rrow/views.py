from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from basket.forms import CartAddProductForm
from .models import Brand, Category, Clothes, Collection, Customer, Order, OrderItem, Review
from .forms import ClothesForm, LoginForm, RegisterForm


class PermissionMessageMixin(PermissionRequiredMixin):
    def handle_no_permission(self):
        messages.error(self.request, 'Недостаточно прав для выполнения действия.')
        return redirect('home')


def home_view(request):
    return render(request, 'home.html')


def info_view(request):
    return render(request, 'info.html')


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_product_form'] = CartAddProductForm(initial={'quantity': 1})
        return context


class ClothesDetailView(DetailView):
    model = Clothes
    template_name = 'clothes/clothes_detail.html'
    context_object_name = 'clothes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_product_form'] = CartAddProductForm(initial={'quantity': 1})
        return context


class ClothesCreateView(LoginRequiredMixin, PermissionMessageMixin, CreateView):
    model = Clothes
    permission_required = 'djS0rrow.add_clothes'
    form_class = ClothesForm
    template_name = 'clothes/clothes_form.html'
    success_url = reverse_lazy('product_list')


class ClothesUpdateView(LoginRequiredMixin, PermissionMessageMixin, UpdateView):
    model = Clothes
    permission_required = 'djS0rrow.change_clothes'
    form_class = ClothesForm
    template_name = 'clothes/clothes_form.html'

    def get_success_url(self):
        return reverse_lazy('product_detail', kwargs={'pk': self.object.pk})


class ClothesDeleteView(LoginRequiredMixin, PermissionMessageMixin, DeleteView):
    model = Clothes
    permission_required = 'djS0rrow.delete_clothes'
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


class CategoryCreateView(LoginRequiredMixin, PermissionMessageMixin, CreateView):
    model = Category
    permission_required = 'djS0rrow.add_category'
    fields = ['name', 'description']
    template_name = 'category/category_form.html'
    success_url = reverse_lazy('category_list')


class CategoryUpdateView(LoginRequiredMixin, PermissionMessageMixin, UpdateView):
    model = Category
    permission_required = 'djS0rrow.change_category'
    fields = ['name', 'description']
    template_name = 'category/category_form.html'

    def get_success_url(self):
        return reverse_lazy('category_detail', kwargs={'pk': self.object.pk})


class CategoryDeleteView(LoginRequiredMixin, PermissionMessageMixin, DeleteView):
    model = Category
    permission_required = 'djS0rrow.delete_category'
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


class CollectionCreateView(LoginRequiredMixin, PermissionMessageMixin, CreateView):
    model = Collection
    permission_required = 'djS0rrow.add_collection'
    fields = ['name', 'description', 'season']
    template_name = 'collection/collection_form.html'
    success_url = reverse_lazy('collection_list')


class CollectionUpdateView(LoginRequiredMixin, PermissionMessageMixin, UpdateView):
    model = Collection
    permission_required = 'djS0rrow.change_collection'
    fields = ['name', 'description', 'season']
    template_name = 'collection/collection_form.html'

    def get_success_url(self):
        return reverse_lazy('collection_detail', kwargs={'pk': self.object.pk})


class CollectionDeleteView(LoginRequiredMixin, PermissionMessageMixin, DeleteView):
    model = Collection
    permission_required = 'djS0rrow.delete_collection'
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


class BrandCreateView(LoginRequiredMixin, PermissionMessageMixin, CreateView):
    model = Brand
    permission_required = 'djS0rrow.add_brand'
    fields = ['name', 'description', 'country', 'logo']
    template_name = 'brand/brand_form.html'
    success_url = reverse_lazy('brand_list')


class BrandUpdateView(LoginRequiredMixin, PermissionMessageMixin, UpdateView):
    model = Brand
    permission_required = 'djS0rrow.change_brand'
    fields = ['name', 'description', 'country', 'logo']
    template_name = 'brand/brand_form.html'

    def get_success_url(self):
        return reverse_lazy('brand_detail', kwargs={'pk': self.object.pk})


class BrandDeleteView(LoginRequiredMixin, PermissionMessageMixin, DeleteView):
    model = Brand
    permission_required = 'djS0rrow.delete_brand'
    template_name = 'brand/brand_confirm_delete.html'
    success_url = reverse_lazy('brand_list')


class CustomerListView(LoginRequiredMixin, PermissionMessageMixin, ListView):
    model = Customer
    permission_required = 'djS0rrow.view_customer'
    template_name = 'customer/customer_list.html'
    context_object_name = 'customers'


class CustomerDetailView(LoginRequiredMixin, PermissionMessageMixin, DetailView):
    model = Customer
    permission_required = 'djS0rrow.view_customer'
    template_name = 'customer/customer_detail.html'
    context_object_name = 'customer'


class CustomerCreateView(LoginRequiredMixin, PermissionMessageMixin, CreateView):
    model = Customer
    permission_required = 'djS0rrow.add_customer'
    fields = ['first_name', 'last_name', 'email', 'phone']
    template_name = 'customer/customer_form.html'
    success_url = reverse_lazy('customer_list')


class CustomerUpdateView(LoginRequiredMixin, PermissionMessageMixin, UpdateView):
    model = Customer
    permission_required = 'djS0rrow.change_customer'
    fields = ['first_name', 'last_name', 'email', 'phone']
    template_name = 'customer/customer_form.html'

    def get_success_url(self):
        return reverse_lazy('customer_detail', kwargs={'pk': self.object.pk})


class CustomerDeleteView(LoginRequiredMixin, PermissionMessageMixin, DeleteView):
    model = Customer
    permission_required = 'djS0rrow.delete_customer'
    template_name = 'customer/customer_confirm_delete.html'
    success_url = reverse_lazy('customer_list')


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'order/order_list.html'
    context_object_name = 'orders'
    queryset = Order.objects.select_related('customer', 'user')

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.has_perm('djS0rrow.view_order'):
            return queryset
        return queryset.filter(user=self.request.user)


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'order/order_detail.html'
    context_object_name = 'order'


    def get_queryset(self):
        queryset = super().get_queryset().select_related('customer', 'user')
        if self.request.user.has_perm('djS0rrow.view_order'):
            return queryset
        return queryset.filter(user=self.request.user)


class OrderCreateView(LoginRequiredMixin, PermissionMessageMixin, CreateView):
    model = Order
    permission_required = 'djS0rrow.add_order'
    fields = ['customer', 'status', 'total_amount']
    template_name = 'order/order_form.html'
    success_url = reverse_lazy('order_list')


class OrderUpdateView(LoginRequiredMixin, PermissionMessageMixin, UpdateView):
    model = Order
    permission_required = 'djS0rrow.change_order'
    fields = ['customer', 'status', 'total_amount']
    template_name = 'order/order_form.html'

    def get_success_url(self):
        return reverse_lazy('order_detail', kwargs={'pk': self.object.pk})


class OrderDeleteView(LoginRequiredMixin, PermissionMessageMixin, DeleteView):
    model = Order
    permission_required = 'djS0rrow.delete_order'
    template_name = 'order/order_confirm_delete.html'
    success_url = reverse_lazy('order_list')


class OrderItemListView(LoginRequiredMixin, PermissionMessageMixin, ListView):
    model = OrderItem
    permission_required = 'djS0rrow.view_orderitem'
    template_name = 'orderitem/orderitem_list.html'
    context_object_name = 'order_items'
    queryset = OrderItem.objects.select_related('order', 'clothes', 'order__customer')


class OrderItemDetailView(LoginRequiredMixin, PermissionMessageMixin, DetailView):
    model = OrderItem
    permission_required = 'djS0rrow.view_orderitem'
    template_name = 'orderitem/orderitem_detail.html'
    context_object_name = 'order_item'


class OrderItemCreateView(LoginRequiredMixin, PermissionMessageMixin, CreateView):
    model = OrderItem
    permission_required = 'djS0rrow.add_orderitem'
    fields = ['order', 'clothes', 'quantity', 'price_at_order']
    template_name = 'orderitem/orderitem_form.html'
    success_url = reverse_lazy('order_item_list')


class OrderItemUpdateView(LoginRequiredMixin, PermissionMessageMixin, UpdateView):
    model = OrderItem
    permission_required = 'djS0rrow.change_orderitem'
    fields = ['order', 'clothes', 'quantity', 'price_at_order']
    template_name = 'orderitem/orderitem_form.html'

    def get_success_url(self):
        return reverse_lazy('order_item_detail', kwargs={'pk': self.object.pk})


class OrderItemDeleteView(LoginRequiredMixin, PermissionMessageMixin, DeleteView):
    model = OrderItem
    permission_required = 'djS0rrow.delete_orderitem'
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


class ReviewCreateView(LoginRequiredMixin, PermissionMessageMixin, CreateView):
    model = Review
    permission_required = 'djS0rrow.add_review'
    fields = ['clothes', 'customer', 'rating', 'text']
    template_name = 'review/review_form.html'
    success_url = reverse_lazy('review_list')


class ReviewUpdateView(LoginRequiredMixin, PermissionMessageMixin, UpdateView):
    model = Review
    permission_required = 'djS0rrow.change_review'
    fields = ['clothes', 'customer', 'rating', 'text']
    template_name = 'review/review_form.html'

    def get_success_url(self):
        return reverse_lazy('review_detail', kwargs={'pk': self.object.pk})


class ReviewDeleteView(LoginRequiredMixin, PermissionMessageMixin, DeleteView):
    model = Review
    permission_required = 'djS0rrow.delete_review'
    template_name = 'review/review_confirm_delete.html'
    success_url = reverse_lazy('review_list')
