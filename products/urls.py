from django.urls import path

from .views      import *

urlpatterns = [
<<<<<<< HEAD
    path("/type", TypeView.as_view()), 
=======
    path("", ProductOptionView.as_view()),
>>>>>>> main
    path("/category", CategoryView.as_view()),
]
