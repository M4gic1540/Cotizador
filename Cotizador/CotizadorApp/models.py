from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    rut = models.CharField(max_length=12, unique=True)
    telefono = models.CharField(max_length=15)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"

from django.contrib.auth import get_user_model
User = get_user_model()

class Cotizacion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    detalles = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)


class Categoria(models.Model):
    """
    Modelo para gestionar categorías dinámicas.

    Puedes agregar, editar o eliminar categorías desde el panel de administración.
    """
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    """
    Modelo de productos con relación a la categoría.

    La categoría se selecciona desde un listado de categorías existentes en la base de datos.
    """
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, related_name='productos')
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.categoria}"