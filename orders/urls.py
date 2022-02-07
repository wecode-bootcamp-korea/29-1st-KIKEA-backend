from django.urls import path

from .views import CartView

urlpatterns = [
    path('carts/<int:product_option_id>', CartView.as_view()),
]