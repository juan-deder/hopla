from django.urls import path
from .views import ImageCreateView

app_name = 'images'

urlpatterns = [
    path('', ImageCreateView.as_view(), name='images')
]