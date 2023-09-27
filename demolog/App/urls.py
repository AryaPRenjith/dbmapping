from django.urls import path
from .views import LogSampleAPIView

urlpatterns = [
    path("logclass", LogSampleAPIView.as_view(), name='logclass'),
]