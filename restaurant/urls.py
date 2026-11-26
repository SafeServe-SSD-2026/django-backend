from rest_framework.routers import SimpleRouter

from restaurant.views import TableViewSet, DishViewSet, OrderViewSet, OrderItemViewSet

router = SimpleRouter()
router.register('tables', TableViewSet, basename='tables')
router.register('dishes', DishViewSet, basename='dishes')
router.register('orders', OrderViewSet, basename='orders')
router.register('order-items', OrderItemViewSet, basename='order-items')

urlpatterns = router.urls