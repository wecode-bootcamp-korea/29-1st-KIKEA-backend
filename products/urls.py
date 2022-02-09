
from django.urls import path

from .views      import *

urlpatterns = [
    path("", ProductOptionView.as_view()),
    path("/category", CategoryView.as_view()),
    path("/review", ReviewView.as_view()),
    path("/product", ProductView.as_view()),
    path("/type", TypeView.as_view()),
]
