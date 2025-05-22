# cotizacion/views.py
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from .models import Cotizacion
from .serializers import CotizacionSerializer
# from .utils import generar_pdf_y_enviar_email


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
    filterset_fields = ('email', 'nombre',)
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
          3. Genera PDF y envía correo al cliente.
        """
        cotizacion = serializer.save()
        if not cotizacion.fecha:
            cotizacion.fecha = timezone.now()
            cotizacion.save()
        # generar_pdf_y_enviar_email(cotizacion)

    def perform_update(self, serializer):
        """
        Actualiza la cotización y reenvía el PDF actualizado.
        """
        cotizacion = serializer.save()
        cotizacion.save()
        # generar_pdf_y_enviar_email(cotizacion)

    def perform_destroy(self, instance):
        """
        Elimina la cotización.
        """
        instance.delete()
        # Aquí podrías enviar notificación o registro de auditoría si lo requieres.
