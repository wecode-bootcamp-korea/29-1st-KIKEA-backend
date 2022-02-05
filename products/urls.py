from django.urls import path

from .views      import *

urlpatterns = [
    path("", ProductOptionView.as_view()),
]
