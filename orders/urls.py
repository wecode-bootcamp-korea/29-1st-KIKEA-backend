from django.urls import path

from orders.views import CartView

urlpatterns = [
    path('/carts', CartView.as_view())
    ]