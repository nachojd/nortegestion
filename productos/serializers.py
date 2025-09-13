from rest_framework import serializers
from .models import Rubro, Marca, Product

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