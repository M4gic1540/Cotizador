from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from decimal import Decimal

# ========================
# Modelo de Usuario Customizado
# ========================
class CustomUser(AbstractUser):
    """
    Extiende el modelo de usuario de Django para incluir campos adicionales
    como RUT, teléfono y un correo único.
    """
    rut = models.CharField(max_length=12, unique=True, help_text="RUT del usuario (único).")
    telefono = models.CharField(max_length=15, help_text="Número de teléfono del usuario.")
    email = models.EmailField(unique=True, help_text="Correo electrónico único del usuario.")

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"


User = get_user_model()


# ========================
# Categoría de Productos
# ========================
class Categoria(models.Model):
    """
    Modelo para representar categorías de productos.
    
    Puedes agregar, editar o eliminar las categorías desde el panel de administración.
    """
    nombre = models.CharField(max_length=50, unique=True, help_text="Nombre de la categoría (único).")

    def __str__(self):
        return self.nombre


# ========================
# Producto
# ========================
class Producto(models.Model):
    """
    Representa un producto vendible que pertenece a una categoría.

    Incluye información como nombre, descripción, precio y stock disponible.
    """
    categoria = models.ForeignKey(
        Categoria, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='productos',
        help_text="Categoría a la que pertenece el producto."
    )
    nombre = models.CharField(max_length=100, help_text="Nombre del producto.")
    descripcion = models.TextField(blank=True, help_text="Descripción detallada del producto (opcional).")
    precio = models.DecimalField(max_digits=10, decimal_places=2, help_text="Precio unitario del producto.")
    stock = models.PositiveIntegerField(help_text="Cantidad disponible en inventario.")
    fecha_creacion = models.DateTimeField(auto_now_add=True, help_text="Fecha de creación del producto.")

    def __str__(self):
        return f"{self.nombre} ({self.categoria})"


# ========================
# Cotización / Factura
# ========================
class Cotizacion(models.Model):
    """
    Encabezado de la factura o cotización.

    Representa una venta con información del cliente, fecha y los productos asociados
    mediante DetalleFactura.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="Usuario que realizó la cotización.")
    fecha = models.DateTimeField(auto_now_add=True, help_text="Fecha y hora de creación de la cotización.")

    def __str__(self):
        return f"Factura #{self.id} - {self.user.get_full_name()}"

    @property
    def subtotal(self):
        """
        Retorna el subtotal sumando los totales de cada producto.
        """
        return sum(detalle.precio_total for detalle in self.detalles.all())

    @property
    def iva(self):
        """
        Calcula el IVA (19%) del subtotal.
        """
        return self.subtotal * Decimal("0.19")

    @property
    def total(self):
        """
        Calcula el total con IVA incluido.
        """
        return self.subtotal + self.iva


# ========================
# Detalle de la Factura
# ========================
class DetalleFactura(models.Model):
    """
    Representa un ítem individual dentro de una cotización o factura.

    Incluye el producto, cantidad y precio unitario al momento de la venta.
    """
    cotizacion = models.ForeignKey(
        Cotizacion, 
        related_name='detalles', 
        on_delete=models.CASCADE,
        help_text="Cotización a la que pertenece este detalle."
    )
    producto = models.ForeignKey(
        Producto, 
        on_delete=models.SET_NULL, 
        null=True, 
        help_text="Producto vendido en este detalle."
    )
    cantidad = models.PositiveIntegerField(help_text="Cantidad del producto vendido.")
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, help_text="Precio unitario aplicado.")

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre if self.producto else 'Producto eliminado'}"

    @property
    def precio_total(self):
        """
        Devuelve el total de este ítem (cantidad * precio unitario).
        """
        return self.cantidad * self.precio_unitario
