from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from decimal import Decimal

class Rubro(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Multi-tenant
    nombre = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Rubros"
        unique_together = ['user', 'nombre']  # Unique per user

class Marca(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Multi-tenant
    nombre = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

    class Meta:
        unique_together = ['user', 'nombre']  # Unique per user

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Multi-tenant
    codigo = models.CharField(max_length=20)
    nombre = models.CharField(max_length=200)
    rubro = models.ForeignKey(Rubro, on_delete=models.CASCADE)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    
    # Precios
    precio_costo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    precio_lista2 = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True)
    precio_lista3 = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True)
    
    # Stock
    stock_actual = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    stock_minimo = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    
    
    observaciones = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

    class Meta:
        unique_together = ['user', 'codigo']  # Unique per user
    

    

class Cliente(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Multi-tenant
    nombre = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.TextField(blank=True)
    cuit = models.CharField(max_length=13, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.nombre

class Quote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Multi-tenant
    numero = models.CharField(max_length=20)
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

    class Meta:
        unique_together = ['user', 'numero']  # Unique per user
    
    def calcular_totales(self):
        total = Decimal('0')
        
        for item in self.items.all():
            total += item.subtotal
        
        self.total = total
        self.save()

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
