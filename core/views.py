from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.db import models
import os
import logging
from .models import Rubro, Marca, Product, Cliente, Quote, QuoteItem
from .serializers import (
    RubroSerializer, MarcaSerializer, ProductSerializer, ProductUpdateSerializer,
    ClienteSerializer, QuoteSerializer, QuoteCreateSerializer
)
from .utils import create_pdf_response

logger = logging.getLogger(__name__)

class FrontendView(TemplateView):
    template_name = 'core/index.html'

class RubroViewSet(viewsets.ModelViewSet):
    serializer_class = RubroSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre']

    def get_queryset(self):
        return Rubro.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class MarcaViewSet(viewsets.ModelViewSet):
    serializer_class = MarcaSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre']

    def get_queryset(self):
        return Marca.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['rubro', 'marca', 'activo', 'rubro__nombre', 'marca__nombre']
    search_fields = ['codigo', 'nombre', 'rubro__nombre', 'marca__nombre']
    ordering_fields = ['codigo', 'nombre', 'precio_venta', 'stock_actual']
    ordering = ['codigo']

    def get_queryset(self):
        # CRÍTICO: Filtrar por usuario en TODAS las operaciones
        return Product.objects.filter(
            user=self.request.user,
            activo=True
        )

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return ProductUpdateSerializer
        return ProductSerializer

    def perform_create(self, serializer):
        # Asignar usuario automáticamente al crear
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        # Mantener usuario al actualizar
        serializer.save(user=self.request.user)

    def retrieve(self, request, pk=None):
        """Override retrieve to add debugging"""
        logger.info(f"Usuario {request.user.email} intentando acceder producto ID {pk}")
        try:
            product = self.get_queryset().get(pk=pk)
            serializer = self.get_serializer(product)
            logger.info(f"Producto {pk} encontrado para usuario {request.user.email}")
            return Response(serializer.data)
        except Product.DoesNotExist:
            logger.error(f"Producto {pk} no encontrado para usuario {request.user.email}")
            return Response({"error": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        """Productos con stock bajo"""
        products = self.get_queryset().filter(
            stock_actual__lte=models.F('stock_minimo')
        )
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)


class ClienteViewSet(viewsets.ModelViewSet):
    serializer_class = ClienteSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre', 'email', 'telefono', 'cuit']

    def get_queryset(self):
        return Cliente.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class QuoteViewSet(viewsets.ModelViewSet):
    serializer_class = QuoteSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['cliente', 'fecha']
    search_fields = ['numero', 'cliente__nombre']

    def get_queryset(self):
        return Quote.objects.filter(user=self.request.user, activo=True)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return QuoteCreateSerializer
        return QuoteSerializer
    
    @action(detail=True, methods=['post'])
    def duplicate(self, request, pk=None):
        """Duplicar presupuesto"""
        quote = self.get_object()
        new_quote_data = {
            'cliente': quote.cliente.id,
            'fecha_vencimiento': quote.fecha_vencimiento,
            'observaciones': f"Copia de {quote.numero} - {quote.observaciones}",
            'items': []
        }
        
        for item in quote.items.all():
            item_data = {
                'producto': item.producto.id if item.producto else None,
                'servicio': None,
                'cantidad': item.cantidad,
                'precio_unitario': item.precio_unitario,
            }
            new_quote_data['items'].append(item_data)
        
        serializer = QuoteCreateSerializer(data=new_quote_data)
        if serializer.is_valid():
            new_quote = serializer.save()
            response_serializer = QuoteSerializer(new_quote)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def pdf(self, request, pk=None):
        """Generar PDF del presupuesto"""
        quote = self.get_object()
        return create_pdf_response(quote)
    
    @action(detail=True, methods=['post'])
    def whatsapp(self, request, pk=None):
        """Compartir por WhatsApp"""
        quote = self.get_object()
        phone = request.data.get('phone')
        if not phone:
            return Response(
                {"error": "Phone number required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # TODO: Implementar envío por WhatsApp
        message = f"Presupuesto {quote.numero} - Total: ${quote.total}"
        whatsapp_url = f"https://wa.me/{phone}?text={message}"
        
        return Response({
            "whatsapp_url": whatsapp_url,
            "message": message
        })
