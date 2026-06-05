from django.urls import path

from .views import (
    basket_add_view,
    basket_clear_view,
    basket_detail_view,
    basket_remove_view,
    basket_update_view,
    order_create_view,
)


urlpatterns = [
    path('cart/', basket_detail_view, name='cart_view'),
    path('cart/add/<int:pk>/', basket_add_view, name='cart_add'),
    path('cart/update/<int:pk>/', basket_update_view, name='cart_update'),
    path('cart/remove/<int:pk>/', basket_remove_view, name='cart_remove'),
    path('cart/clear/', basket_clear_view, name='cart_clear'),
    path('cart/checkout/', order_create_view, name='cart_checkout'),
    path('cart/create-order/', order_create_view, name='create_order_from_cart'),
]

