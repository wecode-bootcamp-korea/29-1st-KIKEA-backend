from django.urls import path

from orders.views import CartView, OrderView

urlpatterns = [
    path('', OrderView.as_view()),
    path('/<int:order_item_id>', OrderView.as_view()),
    path('/carts', CartView.as_view()),
    path('/carts/<int:product_option_id>', CartView.as_view()),
    ]