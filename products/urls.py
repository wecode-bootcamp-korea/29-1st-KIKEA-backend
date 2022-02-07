from django.urls import path

from .views      import *

urlpatterns = [
    path("/type"    , TypeView.as_view()), 
]
