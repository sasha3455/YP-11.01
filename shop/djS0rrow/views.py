from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .models import Brand, Category, Clothes, Collection, Customer, Order, OrderItem, Review
from .forms import ClothesForm


def home_view(request):
    return render(request, 'home.html')


def info_view(request):
    return render(request, 'info.html')


def cart_view(request):
    return render(request, 'cart.html')


class ClothesListView(ListView):
    model = Clothes
    template_name = 'clothes/clothes_list.html'
    context_object_name = 'clothes'
    queryset = Clothes.objects.select_related('category', 'brand').filter(is_exists=True)


class ClothesDetailView(DetailView):
    model = Clothes
    template_name = 'clothes/clothes_detail.html'
    context_object_name = 'clothes'


class ClothesCreateView(CreateView):
    model = Clothes
    form_class = ClothesForm
    template_name = 'clothes/clothes_form.html'
    success_url = reverse_lazy('product_list')


class ClothesUpdateView(UpdateView):
    model = Clothes
    form_class = ClothesForm
    template_name = 'clothes/clothes_form.html'

    def get_success_url(self):
        return reverse_lazy('product_detail', kwargs={'pk': self.object.pk})


class ClothesDeleteView(DeleteView):
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


class CategoryCreateView(CreateView):
    model = Category
    fields = ['name', 'description']
    template_name = 'category/category_form.html'
    success_url = reverse_lazy('category_list')


class CategoryUpdateView(UpdateView):
    model = Category
    fields = ['name', 'description']
    template_name = 'category/category_form.html'

    def get_success_url(self):
        return reverse_lazy('category_detail', kwargs={'pk': self.object.pk})


class CategoryDeleteView(DeleteView):
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


class CollectionCreateView(CreateView):
    model = Collection
    fields = ['name', 'description', 'season']
    template_name = 'collection/collection_form.html'
    success_url = reverse_lazy('collection_list')


class CollectionUpdateView(UpdateView):
    model = Collection
    fields = ['name', 'description', 'season']
    template_name = 'collection/collection_form.html'

    def get_success_url(self):
        return reverse_lazy('collection_detail', kwargs={'pk': self.object.pk})


class CollectionDeleteView(DeleteView):
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


class BrandCreateView(CreateView):
    model = Brand
    fields = ['name', 'description', 'country', 'logo']
    template_name = 'brand/brand_form.html'
    success_url = reverse_lazy('brand_list')


class BrandUpdateView(UpdateView):
    model = Brand
    fields = ['name', 'description', 'country', 'logo']
    template_name = 'brand/brand_form.html'

    def get_success_url(self):
        return reverse_lazy('brand_detail', kwargs={'pk': self.object.pk})


class BrandDeleteView(DeleteView):
    model = Brand
    template_name = 'brand/brand_confirm_delete.html'
    success_url = reverse_lazy('brand_list')


class CustomerListView(ListView):
    model = Customer
    template_name = 'customer/customer_list.html'
    context_object_name = 'customers'


class CustomerDetailView(DetailView):
    model = Customer
    template_name = 'customer/customer_detail.html'
    context_object_name = 'customer'


class CustomerCreateView(CreateView):
    model = Customer
    fields = ['first_name', 'last_name', 'email', 'phone']
    template_name = 'customer/customer_form.html'
    success_url = reverse_lazy('customer_list')


class CustomerUpdateView(UpdateView):
    model = Customer
    fields = ['first_name', 'last_name', 'email', 'phone']
    template_name = 'customer/customer_form.html'

    def get_success_url(self):
        return reverse_lazy('customer_detail', kwargs={'pk': self.object.pk})


class CustomerDeleteView(DeleteView):
    model = Customer
    template_name = 'customer/customer_confirm_delete.html'
    success_url = reverse_lazy('customer_list')


class OrderListView(ListView):
    model = Order
    template_name = 'order/order_list.html'
    context_object_name = 'orders'
    queryset = Order.objects.select_related('customer')


class OrderDetailView(DetailView):
    model = Order
    template_name = 'order/order_detail.html'
    context_object_name = 'order'


class OrderCreateView(CreateView):
    model = Order
    fields = ['customer', 'status', 'total_amount']
    template_name = 'order/order_form.html'
    success_url = reverse_lazy('order_list')


class OrderUpdateView(UpdateView):
    model = Order
    fields = ['customer', 'status', 'total_amount']
    template_name = 'order/order_form.html'

    def get_success_url(self):
        return reverse_lazy('order_detail', kwargs={'pk': self.object.pk})


class OrderDeleteView(DeleteView):
    model = Order
    template_name = 'order/order_confirm_delete.html'
    success_url = reverse_lazy('order_list')


class OrderItemListView(ListView):
    model = OrderItem
    template_name = 'orderitem/orderitem_list.html'
    context_object_name = 'order_items'
    queryset = OrderItem.objects.select_related('order', 'clothes', 'order__customer')


class OrderItemDetailView(DetailView):
    model = OrderItem
    template_name = 'orderitem/orderitem_detail.html'
    context_object_name = 'order_item'


class OrderItemCreateView(CreateView):
    model = OrderItem
    fields = ['order', 'clothes', 'quantity', 'price_at_order']
    template_name = 'orderitem/orderitem_form.html'
    success_url = reverse_lazy('order_item_list')


class OrderItemUpdateView(UpdateView):
    model = OrderItem
    fields = ['order', 'clothes', 'quantity', 'price_at_order']
    template_name = 'orderitem/orderitem_form.html'

    def get_success_url(self):
        return reverse_lazy('order_item_detail', kwargs={'pk': self.object.pk})


class OrderItemDeleteView(DeleteView):
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
