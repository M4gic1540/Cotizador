from django.http import FileResponse
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from .models import Cotizacion, CustomUser, Categoria, Producto
from .serializers import CotizacionSerializer, CustomUserSerializer, CategoriaSerializer, ProductoSerializer
from .utils import generar_pdf
import pandas as pd
from django.http import HttpResponse


class CotizacionViewSet(viewsets.ModelViewSet):
    """
    ViewSet para manejar operaciones CRUD sobre Cotizacion.

    Funcionalidades añadidas:
      - Filtrado por campos: email, nombre.
      - Rango de fechas: start_date, end_date (consulta GET).
      - Búsqueda por detalles (SearchFilter).
      - Ordenamiento por ID,fecha y precio (OrderingFilter).
      - Generación de PDF y envío de correo al crear.
    """
    queryset = Cotizacion.objects.all()
    serializer_class = CotizacionSerializer

    # Configuración de filtros
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    search_fields = ('detalles',)
    ordering_fields = ('id', 'fecha', 'precio')
    ordering = ('-fecha',)

    def get_queryset(self):
        """
        Retorna el conjunto de cotizaciones aplicando filtros de fecha opcionales.
        Parámetros GET admitidos:
          - start_date: YYYY-MM-DD
          - end_date: YYYY-MM-DD
        """
        queryset = super().get_queryset()
        start = self.request.query_params.get('start_date')
        end = self.request.query_params.get('end_date')
        if start:
            queryset = queryset.filter(fecha__date__gte=start)
        if end:
            queryset = queryset.filter(fecha__date__lte=end)
        return queryset

    def perform_create(self, serializer):
        """
        Al crear una cotización:
          1. Guarda la instancia.
          2. Asigna fecha actual si no existe.
        """
        cotizacion = serializer.save()
        if not cotizacion.fecha:
            cotizacion.fecha = timezone.now()
            cotizacion.save()

    @action(detail=True, methods=['get'])
    def descargar_pdf(self, request, pk=None):
        """
        Genera el PDF de la cotización y permite descargarlo.
        """
        cotizacion = self.get_object()
        buffer = generar_pdf(cotizacion)
        return FileResponse(buffer, as_attachment=True, filename=f'cotizacion_{cotizacion.id}.pdf')

    def perform_update(self, serializer):
        """
        Actualiza la cotización.
        """
        cotizacion = serializer.save()
        cotizacion.save()

    def perform_destroy(self, instance):
        """
        Elimina la cotización.
        """
        instance.delete()
        # Aquí podrías enviar notificación o registro de auditoría si lo requieres.

    @action(detail=False, methods=["get"])
    def exportar_a_excel_cotizaciones(self, request):
        """
        Exporta las cotizaciones filtradas como un archivo Excel.
        Soporta filtros por fecha como en `get_queryset`.
        """
        queryset = self.get_queryset()  # aplica filtros si están en la URL
        data = []

        for c in queryset:
            for detalle in c.detalles.all():
                data.append({
                    "ID Cotización": c.id,
                    "Fecha": c.fecha.strftime("%d-%m-%Y"),
                    "Cliente": f"{c.user.first_name} {c.user.last_name}",
                    "Email": c.user.email,
                    "Producto": detalle.producto.nombre if detalle.producto else "Eliminado",
                    "Cantidad": detalle.cantidad,
                    "Precio Unitario": float(detalle.precio_unitario),
                    "Precio Total": float(detalle.precio_total),
                })

        df = pd.DataFrame(data)
        buffer = pd.ExcelWriter("cotizaciones.xlsx", engine='openpyxl')
        df.to_excel(buffer, index=False, sheet_name="Cotizaciones")
        buffer.close()

        # Devolver como archivo descargable
        with open("cotizaciones.xlsx", "rb") as f:
            response = HttpResponse(f.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="cotizaciones.xlsx"'
            return response


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestión de usuarios personalizados.

    Funcionalidades:
    - Filtrado por ID, nombre, apellido, RUT y correo electrónico.
    - Búsqueda por nombre y correo.
    - Ordenamiento opcional.
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ['id', 'first_name', 'last_name', 'rut', 'email']
    search_fields = ['first_name', 'last_name', 'email', 'rut']
    ordering_fields = ['id', 'first_name', 'last_name']
    ordering = ['id']

    @action(detail=False, methods=['get'])
    def exportar_a_excel_usuarios(self, request):
        """
        Exporta los usuarios como un archivo Excel.
        """
        queryset = self.get_queryset()
        data = []

        for user in queryset:
            data.append({
                "ID": user.id,
                "Nombre": user.first_name,
                "Apellido": user.last_name,
                "RUT": user.rut,
                "Email": user.email,
            })

        df = pd.DataFrame(data)
        buffer = pd.ExcelWriter("usuarios.xlsx", engine='openpyxl')
        df.to_excel(buffer, index=False, sheet_name="Usuarios")
        buffer.close()

        # Devolver como archivo descargable
        with open("usuarios.xlsx", "rb") as f:
            response = HttpResponse(f.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="usuarios.xlsx"'
            return response

class CategoriaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para listar, crear y administrar categorías.
    """
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer


class ProductoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar productos.
    """
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['categoria', 'nombre', 'precio']
    search_fields = ['nombre', 'descripcion']
    ordering_fields = ['id', 'nombre', 'precio']

    @action(detail=False, methods=['get'])
    def exportar_a_excel_productos(self, request):
        """
        Exporta los productos como un archivo Excel.
        """
        queryset = self.get_queryset()
        data = []

        for producto in queryset:
            data.append({
                "ID": producto.id,
                "Nombre": producto.nombre,
                "Descripción": producto.descripcion,
                "Precio": float(producto.precio),
                "Categoría": producto.categoria.nombre if producto.categoria else "Sin categoría",
                "Stock": producto.stock,
            })

        df = pd.DataFrame(data)
        buffer = pd.ExcelWriter("productos.xlsx", engine='openpyxl')
        df.to_excel(buffer, index=False, sheet_name="Productos")
        buffer.close()

        # Devolver como archivo descargable
        with open("productos.xlsx", "rb") as f:
            response = HttpResponse(f.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="productos.xlsx"'
            return response