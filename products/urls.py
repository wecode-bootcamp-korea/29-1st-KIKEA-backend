from django.urls import path

from .views      import *

urlpatterns = [
    path("/type", TypeView.as_view()), 
    path("", ProductOptionView.as_view()),
    path("/category", CategoryView.as_view()),
]
