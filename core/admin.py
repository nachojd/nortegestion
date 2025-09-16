from django.contrib import admin
from .models import Rubro, Marca, Product, Cliente, Quote, QuoteItem

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


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'email', 'telefono', 'created_at']
    search_fields = ['nombre', 'email', 'telefono', 'cuit']

class QuoteItemInline(admin.TabularInline):
    model = QuoteItem
    extra = 1
    autocomplete_fields = ['producto']

@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ['numero', 'cliente', 'fecha', 'total', 'activo']
    list_filter = ['fecha', 'activo']
    search_fields = ['numero', 'cliente__nombre']
    inlines = [QuoteItemInline]
    readonly_fields = ['total']
