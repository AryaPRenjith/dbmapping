from django.urls import path
from .views import RoleAPIView

urlpatterns = [
    path("Rolecheck/", RoleAPIView.as_view(), name='Rolecheck'),
]