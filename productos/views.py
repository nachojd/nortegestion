from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db import models

from .models import Rubro, Marca, Product
from .serializers import RubroSerializer, MarcaSerializer, ProductSerializer

class RubroViewSet(viewsets.ModelViewSet):
    queryset = Rubro.objects.all()
    serializer_class = RubroSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre']

class MarcaViewSet(viewsets.ModelViewSet):
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre']

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(activo=True)
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['rubro', 'marca', 'activo', 'rubro__nombre', 'marca__nombre']
    search_fields = ['codigo', 'nombre', 'rubro__nombre', 'marca__nombre']
    ordering_fields = ['codigo', 'nombre', 'precio_venta', 'stock_actual']
    ordering = ['codigo']
    
    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        """Productos con stock bajo"""
        products = Product.objects.filter(
            activo=True,
            stock_actual__lte=models.F('stock_minimo')
        )
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
