from rest_framework.routers import DefaultRouter

from .views import ( BrandViewSet,CategoryViewSet, ClothesViewSet, CollectionViewSet, CustomerViewSet, OrderItemViewSet, OrderViewSet, ReviewViewSet,)

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='api_categories')
router.register('collections', CollectionViewSet, basename='api_collections')
router.register('brands', BrandViewSet, basename='api_brands')
router.register('clothes', ClothesViewSet, basename='api_clothes')
router.register('customers', CustomerViewSet, basename='api_customers')
router.register('orders', OrderViewSet, basename='api_orders')
router.register('order-items', OrderItemViewSet, basename='api_order_items')
router.register('reviews', ReviewViewSet, basename='api_reviews')

urlpatterns = router.urls
