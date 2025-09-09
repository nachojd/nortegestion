from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.db import models
import os
from .models import Rubro, Marca, Product, Cliente, Quote, QuoteItem
from .serializers import (
    RubroSerializer, MarcaSerializer, ProductSerializer, ProductUpdateSerializer,
    ClienteSerializer, QuoteSerializer, QuoteCreateSerializer
)
from .utils import create_pdf_response

class FrontendView(TemplateView):
    def get(self, request):
        # Read and serve the frontend HTML file
        frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend-demo.html')
        try:
            with open(frontend_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return HttpResponse(content, content_type='text/html')
        except FileNotFoundError:
            return HttpResponse('<h1>Frontend no encontrado</h1>', content_type='text/html')

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
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['rubro', 'marca', 'activo']
    search_fields = ['codigo', 'nombre']
    
    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return ProductUpdateSerializer
        return ProductSerializer
        
    def perform_update(self, serializer):
        # Save only the allowed fields without touching timestamps
        serializer.save()
    
    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        """Productos con stock bajo"""
        products = Product.objects.filter(
            activo=True,
            stock_actual__lte=models.F('stock_minimo')
        )
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre', 'email', 'telefono', 'cuit']

class QuoteViewSet(viewsets.ModelViewSet):
    queryset = Quote.objects.filter(activo=True)
    serializer_class = QuoteSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['cliente', 'fecha']
    search_fields = ['numero', 'cliente__nombre']
    
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
