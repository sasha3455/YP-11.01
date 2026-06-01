from rest_framework import filters, viewsets

from djS0rrow.models import Brand, Category, Clothes, Collection, Customer, Order, OrderItem, Review
from .permission import CustomPermissions, PaginationPage
from .serializers import ( BrandSerializer, CategorySerializer, ClothesSerializer, CollectionSerializer, CustomerSerializer, OrderItemSerializer, OrderSerializer, ReviewSerializer,)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PaginationPage
    permission_classes = [CustomPermissions]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']


class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    pagination_class = PaginationPage
    permission_classes = [CustomPermissions]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description', 'season']


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    pagination_class = PaginationPage
    permission_classes = [CustomPermissions]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description', 'country']


class ClothesViewSet(viewsets.ModelViewSet):
    queryset = Clothes.objects.all()
    serializer_class = ClothesSerializer
    pagination_class = PaginationPage
    permission_classes = [CustomPermissions]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description', 'size', 'color']


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    pagination_class = PaginationPage
    permission_classes = [CustomPermissions]
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name', 'email', 'phone']


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = PaginationPage
    permission_classes = [CustomPermissions]
    filter_backends = [filters.SearchFilter]
    search_fields = ['status']


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    pagination_class = PaginationPage
    permission_classes = [CustomPermissions]
    filter_backends = [filters.SearchFilter]
    search_fields = ['quantity']


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = PaginationPage
    permission_classes = [CustomPermissions]
    filter_backends = [filters.SearchFilter]
    search_fields = ['rating', 'text']
