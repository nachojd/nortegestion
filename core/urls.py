from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from .views import (
    RubroViewSet, MarcaViewSet, ProductViewSet,
    ClienteViewSet, QuoteViewSet, FrontendView
)

router = DefaultRouter()
router.register(r'rubros', RubroViewSet)
router.register(r'marcas', MarcaViewSet)
router.register(r'products', ProductViewSet)
router.register(r'clientes', ClienteViewSet)
router.register(r'quotes', QuoteViewSet)

urlpatterns = [
    path('', FrontendView.as_view(), name='frontend'),
    path('api/', include(router.urls)),
]