from django.urls import path
from .views import FrontendView, api_info

urlpatterns = [
    path('', FrontendView.as_view(), name='frontend'),
    path('api/', api_info, name='api_info'),
]