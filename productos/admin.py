from django.contrib import admin
from .models import Rubro, Marca, Product

@admin.register(Rubro)
class RubroAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'created_at']
    search_fields = ['nombre']

@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'created_at']
    search_fields = ['nombre']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'rubro', 'marca', 'precio_venta', 'stock_actual', 'activo']
    list_filter = ['rubro', 'marca', 'activo']
    search_fields = ['codigo', 'nombre']
    list_editable = ['precio_venta', 'stock_actual', 'activo']
