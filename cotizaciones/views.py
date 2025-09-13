from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Quote, QuoteItem
from .serializers import QuoteSerializer, QuoteCreateSerializer

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
