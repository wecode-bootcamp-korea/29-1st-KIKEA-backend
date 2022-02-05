from django.urls import path

from .views      import *

urlpatterns = [
    path("/review", ReviewView.as_view())
]
