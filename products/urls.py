from django.urls import path

from .views      import *

urlpatterns = [
    path("/category", CategoryView.as_view()),
    path("/review", ReviewView.as_view())
]