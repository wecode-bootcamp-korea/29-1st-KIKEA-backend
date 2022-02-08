<<<<<<< HEAD
from django.urls import path

from .views      import *

urlpatterns = [
    path("/review", ReviewView.as_view())
]
=======
from django.urls import path

from .views      import *

urlpatterns = [
    path("/category", CategoryView.as_view()),
]
>>>>>>> main
