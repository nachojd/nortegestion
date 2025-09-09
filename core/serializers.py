from rest_framework import serializers
from .models import Rubro, Marca, Product, Cliente, Quote, QuoteItem

class RubroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rubro
        fields = '__all__'

class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    rubro_nombre = serializers.CharField(source='rubro.nombre', read_only=True)
    marca_nombre = serializers.CharField(source='marca.nombre', read_only=True)
    
    class Meta:
        model = Product
        fields = '__all__'

class ProductUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['precio_costo', 'precio_venta', 'precio_lista2', 'precio_lista3', 'stock_actual', 'stock_minimo']
    
    def update(self, instance, validated_data):
        # Update only specific fields, avoiding timestamp issues
        for field, value in validated_data.items():
            setattr(instance, field, value)
        # Use update_fields to avoid touching created_at
        update_fields = list(validated_data.keys()) + ['updated_at']
        instance.save(update_fields=update_fields)
        return instance


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class QuoteItemSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = QuoteItem
        fields = '__all__'

class QuoteSerializer(serializers.ModelSerializer):
    items = QuoteItemSerializer(many=True, read_only=True)
    cliente_nombre = serializers.CharField(source='cliente.nombre', read_only=True)
    
    class Meta:
        model = Quote
        fields = '__all__'

class QuoteItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuoteItem
        fields = ['producto', 'cantidad']

class QuoteCreateSerializer(serializers.ModelSerializer):
    items = QuoteItemCreateSerializer(many=True)
    
    class Meta:
        model = Quote
        fields = ['cliente', 'fecha_vencimiento', 'observaciones', 'items']
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        
        # Generate quote number
        last_quote = Quote.objects.filter(numero__startswith='P').order_by('-numero').first()
        if last_quote:
            last_num = int(last_quote.numero[1:])
            new_num = f"P{last_num + 1:05d}"
        else:
            new_num = "P00001"
        
        quote = Quote.objects.create(numero=new_num, **validated_data)
        
        for item_data in items_data:
            QuoteItem.objects.create(quote=quote, **item_data)
        
        quote.calcular_totales()
        return quote