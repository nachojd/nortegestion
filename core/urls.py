from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RubroViewSet, MarcaViewSet, ProductViewSet,
    ClienteViewSet, QuoteViewSet
)

router = DefaultRouter()
router.register(r'rubros', RubroViewSet)
router.register(r'marcas', MarcaViewSet)
router.register(r'products', ProductViewSet)
router.register(r'clientes', ClienteViewSet)
router.register(r'quotes', QuoteViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]