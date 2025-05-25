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
