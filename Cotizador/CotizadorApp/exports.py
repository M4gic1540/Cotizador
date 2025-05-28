# cotizaciones/exports.py

from django.http import HttpResponse, FileResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import Cotizacion
from .utils import generar_pdf
import pandas as pd


class ExportarCotizacionesExcel(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        cotizaciones = Cotizacion.objects.filter(user=user)
        data = []

        for c in cotizaciones:
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
            df.to_excel(writer, index=False)

        with open(file_name, "rb") as f:
            response = HttpResponse(
                f.read(),
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = f'attachment; filename="{file_name}"'
            return response


class ExportarCotizacionPDF(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            cotizacion = Cotizacion.objects.get(pk=pk, user=request.user)
        except Cotizacion.DoesNotExist:
            return HttpResponse("Cotización no encontrada", status=404)

        buffer = generar_pdf(cotizacion)
        return FileResponse(buffer, as_attachment=True, filename=f"cotizacion_{cotizacion.id}.pdf")
