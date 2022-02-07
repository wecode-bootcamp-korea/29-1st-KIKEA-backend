from django.urls import path

from .views import CartView

urlpatterns = [
    path('/carts', CartView.as_view()),
    path('/carts/<int:product_option_id>', CartView.as_view()),
    ]
