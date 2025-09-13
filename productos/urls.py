from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RubroViewSet, MarcaViewSet, ProductViewSet

router = DefaultRouter()
router.register(r'rubros', RubroViewSet)
router.register(r'marcas', MarcaViewSet)
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
]