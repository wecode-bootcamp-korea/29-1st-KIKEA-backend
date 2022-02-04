from django.urls import path

# from .views import CartView
from .views import OrderView

urlpatterns = [
    path('', OrderView.as_view()),
    # path('/carts', CartView.as_view()),
    # path('/carts/<int:product_option_id>', CartView.as_view()),
]