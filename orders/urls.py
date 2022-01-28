from django.urls import path

from .views import CartView

urlpatterns = [
    path('/carts', CartView.as_view()),
    ]