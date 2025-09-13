from rest_framework import serializers
from .models import Quote, QuoteItem
from clientes.serializers import ClienteSerializer
from productos.serializers import ProductSerializer

class QuoteItemSerializer(serializers.ModelSerializer):
    producto_info = ProductSerializer(source='producto', read_only=True)
    
    class Meta:
        model = QuoteItem
        fields = '__all__'

class QuoteSerializer(serializers.ModelSerializer):
    cliente_info = ClienteSerializer(source='cliente', read_only=True)
    items = QuoteItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Quote
        fields = '__all__'

class QuoteCreateSerializer(serializers.ModelSerializer):
    items = QuoteItemSerializer(many=True)
    
    class Meta:
        model = Quote
        fields = '__all__'
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        quote = Quote.objects.create(**validated_data)
        for item_data in items_data:
            QuoteItem.objects.create(quote=quote, **item_data)
        return quote
