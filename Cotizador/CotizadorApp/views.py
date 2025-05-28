from django.http import FileResponse, HttpResponse
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from .models import Cotizacion, CustomUser, Categoria, Producto
from .serializers import CotizacionSerializer, CustomUserSerializer, CategoriaSerializer, ProductoSerializer
from .utils import generar_pdf
import pandas as pd


class CotizacionViewSet(viewsets.ModelViewSet):
    """
    ViewSet para manejar cotizaciones:
    - CRUD
    - Filtros por usuario, fecha, búsqueda y orden
    - Exportación a PDF y Excel
    """
    serializer_class = CotizacionSerializer
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['detalles__producto__nombre']
    ordering_fields = ['id', 'fecha']
    ordering = ['-fecha']

    def get_queryset(self):
        """
        Devuelve solo las cotizaciones del usuario autenticado.
        """
        user = self.request.user
        queryset = Cotizacion.objects.filter(user=user)

        start = self.request.query_params.get('start_date')
        end = self.request.query_params.get('end_date')
        if start:
            queryset = queryset.filter(fecha__date__gte=start)
        if end:
            queryset = queryset.filter(fecha__date__lte=end)
        return queryset

    def perform_create(self, serializer):
        """
        Asigna automáticamente el usuario autenticado y la fecha si no fue proporcionada.
        """
        cotizacion = serializer.save(user=self.request.user)
        if not cotizacion.fecha:
            cotizacion.fecha = timezone.now()
            cotizacion.save()

    @action(detail=True, methods=['get'])
    def descargar_pdf(self, request, pk=None):
        """
        Devuelve un archivo PDF de la cotización.
        """
        cotizacion = self.get_object()
        buffer = generar_pdf(cotizacion)
        return FileResponse(buffer, as_attachment=True, filename=f'cotizacion_{cotizacion.id}.pdf')

    @action(detail=False, methods=["get"])
    def exportar_a_excel_cotizaciones(self, request):
        """
        Exporta todas las cotizaciones del usuario autenticado a un archivo Excel.
        """
        queryset = self.get_queryset()
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
        file_name = "cotizaciones.xlsx"
        with pd.ExcelWriter(file_name, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name="Cotizaciones")

        with open(file_name, "rb") as f:
            response = HttpResponse(f.read(
            ), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename="{file_name}"'
            return response


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet para la gestión de usuarios personalizados.
    Soporta filtrado, búsqueda, ordenamiento y exportación.
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['id', 'first_name', 'last_name', 'rut', 'email']
    search_fields = ['first_name', 'last_name', 'email', 'rut']
    ordering_fields = ['id', 'first_name', 'last_name']
    ordering = ['id']

    @action(detail=False, methods=['get'])
    def exportar_a_excel_usuarios(self, request):
        """
        Exporta todos los usuarios a un archivo Excel.
        """
        queryset = self.get_queryset()
        data = [{
            "ID": user.id,
            "Nombre": user.first_name,
            "Apellido": user.last_name,
            "RUT": user.rut,
            "Email": user.email,
        } for user in queryset]

        df = pd.DataFrame(data)
        file_name = "usuarios.xlsx"
        with pd.ExcelWriter(file_name, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name="Usuarios")

        with open(file_name, "rb") as f:
            response = HttpResponse(f.read(
            ), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename="{file_name}"'
            return response


class CategoriaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar categorías.
    """
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer


class ProductoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar productos con filtro y exportación a Excel.
    """
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['categoria', 'nombre', 'precio']
    search_fields = ['nombre', 'descripcion']
    ordering_fields = ['id', 'nombre', 'precio']

    @action(detail=False, methods=['get'])
    def exportar_a_excel_productos(self, request):
        """
        Exporta todos los productos a un archivo Excel.
        """
        queryset = self.get_queryset()
        data = [{
            "ID": p.id,
            "Nombre": p.nombre,
            "Descripción": p.descripcion,
            "Precio": float(p.precio),
            "Categoría": p.categoria.nombre if p.categoria else "Sin categoría",
            "Stock": p.stock,
        } for p in queryset]

        df = pd.DataFrame(data)
        file_name = "productos.xlsx"
        with pd.ExcelWriter(file_name, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name="Productos")

        with open(file_name, "rb") as f:
            response = HttpResponse(f.read(
            ), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename="{file_name}"'
            return response
