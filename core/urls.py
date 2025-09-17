from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from django.http import JsonResponse
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    RubroViewSet, MarcaViewSet, ProductViewSet,
    ClienteViewSet, QuoteViewSet
)

router = DefaultRouter()
router.register(r'rubros', RubroViewSet, basename='rubro')
router.register(r'marcas', MarcaViewSet, basename='marca')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'clientes', ClienteViewSet, basename='cliente')
router.register(r'quotes', QuoteViewSet, basename='quote')

def api_info(request):
    return JsonResponse({
        'message': 'NorteGestion API Backend',
        'version': '1.0',
        'endpoints': {
            'products': '/api/products/',
            'rubros': '/api/rubros/',
            'marcas': '/api/marcas/',
            'clientes': '/api/clientes/',
            'quotes': '/api/quotes/',
            'auth_login': '/api/auth/login/',
            'auth_refresh': '/api/auth/refresh/',
        },
        'frontend_url': 'http://5.161.102.34'
    })

urlpatterns = [
    path('', api_info, name='api_info'),
    path('api/', include(router.urls)),
    # Autenticación JWT
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]