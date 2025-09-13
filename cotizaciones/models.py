from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

from clientes.models import Cliente
from productos.models import Product

class Quote(models.Model):
    numero = models.CharField(max_length=20, unique=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    fecha_vencimiento = models.DateField()
    observaciones = models.TextField(blank=True)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Presupuesto {self.numero} - {self.cliente.nombre}"
    
    def calcular_totales(self):
        total = Decimal('0')
        
        for item in self.items.all():
            total += item.subtotal
        
        self.total = total
        self.save()
    
    class Meta:
        verbose_name = "Cotización"
        verbose_name_plural = "Cotizaciones"

class QuoteItem(models.Model):
    quote = models.ForeignKey(Quote, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=200)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    
    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario
    
    def save(self, *args, **kwargs):
        # Auto-populate fields based on product
        if self.producto:
            self.descripcion = self.producto.nombre
            self.precio_unitario = self.producto.precio_venta
        
        super().save(*args, **kwargs)
        self.quote.calcular_totales()
    
    class Meta:
        verbose_name = "Item de Cotización"
        verbose_name_plural = "Items de Cotización"