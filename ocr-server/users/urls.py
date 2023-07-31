from django.urls import path 
from .views import * 

urlpatterns = [
    path("", Users.as_view()),
    path("user/<int:pk>",UserDetail.as_view()),
]