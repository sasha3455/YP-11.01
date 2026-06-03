from rest_framework import serializers

from djS0rrow.models import Brand, Category, Clothes, Collection, Customer, Order, OrderItem, Review


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'name', 'description', 'season']


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'description', 'country', 'logo']


class ClothesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clothes
        fields = ['id', 'name', 'description', 'price', 'size', 'color', 'photo', 'create_date', 'is_exists', 'category', 'collection', 'brand']


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'user', 'first_name', 'last_name', 'email', 'phone']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'customer', 'order_date', 'status', 'total_amount']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'clothes', 'quantity', 'price_at_order']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'clothes', 'customer', 'rating', 'text', 'created_at']
