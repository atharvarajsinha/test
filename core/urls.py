from django.urls import path
from .views import home_view, predict_view, predict_api_view

urlpatterns = [
    path('', home_view, name='home'),
    path('predict/', predict_view, name='predict'),
    path('predict-api/', predict_api_view, name='predict_api'),
]
