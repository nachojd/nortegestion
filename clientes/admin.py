from django.contrib import admin
from .models import Cliente

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'email', 'telefono', 'created_at']
    search_fields = ['nombre', 'email', 'telefono', 'cuit']
