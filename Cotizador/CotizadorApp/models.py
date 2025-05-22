from django.db import models

class Cotizacion(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    detalles = models.TextField()
    cantidad = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)
