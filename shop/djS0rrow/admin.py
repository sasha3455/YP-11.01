from django.contrib import admin

from .models import Brand, Category, Clothes, Collection, Customer, Order, OrderItem, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'season')


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')


@admin.register(Clothes)
class ClothesAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'brand', 'is_exists')
    list_filter = ('category', 'brand', 'is_exists')
    filter_horizontal = ('collection',)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'email', 'phone')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('pk', 'customer', 'order_date', 'status', 'total_amount')
    list_filter = ('status',)
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('pk', 'order', 'clothes', 'quantity', 'price_at_order')
    list_filter = ('order',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('clothes', 'customer', 'rating', 'created_at')
