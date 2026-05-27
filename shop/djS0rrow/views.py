from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Brand, Category, Clothes, Collection, Customer, Order, OrderItem, Review


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


class CategoryListView(ListView):
    model = Category
    template_name = 'category/category_list.html'
    context_object_name = 'categories'


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'category/category_detail.html'
    context_object_name = 'category'


class CollectionListView(ListView):
    model = Collection
    template_name = 'collection/collection_list.html'
    context_object_name = 'collections'


class CollectionDetailView(DetailView):
    model = Collection
    template_name = 'collection/collection_detail.html'
    context_object_name = 'collection'


class BrandListView(ListView):
    model = Brand
    template_name = 'brand/brand_list.html'
    context_object_name = 'brands'


class BrandDetailView(DetailView):
    model = Brand
    template_name = 'brand/brand_detail.html'
    context_object_name = 'brand'


class CustomerListView(ListView):
    model = Customer
    template_name = 'customer/customer_list.html'
    context_object_name = 'customers'


class CustomerDetailView(DetailView):
    model = Customer
    template_name = 'customer/customer_detail.html'
    context_object_name = 'customer'


class OrderListView(ListView):
    model = Order
    template_name = 'order/order_list.html'
    context_object_name = 'orders'
    queryset = Order.objects.select_related('customer')


class OrderDetailView(DetailView):
    model = Order
    template_name = 'order/order_detail.html'
    context_object_name = 'order'


class OrderItemListView(ListView):
    model = OrderItem
    template_name = 'orderitem/orderitem_list.html'
    context_object_name = 'order_items'
    queryset = OrderItem.objects.select_related('order', 'clothes', 'order__customer')


class OrderItemDetailView(DetailView):
    model = OrderItem
    template_name = 'orderitem/orderitem_detail.html'
    context_object_name = 'order_item'


class ReviewListView(ListView):
    model = Review
    template_name = 'review/review_list.html'
    context_object_name = 'reviews'
    queryset = Review.objects.select_related('clothes', 'customer')


class ReviewDetailView(DetailView):
    model = Review
    template_name = 'review/review_detail.html'
    context_object_name = 'review'
