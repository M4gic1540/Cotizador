from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from decimal import Decimal


def generar_pdf(cotizacion):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # Encabezado
    elements.append(Paragraph("<b>Factura</b>", styles['Title']))
    elements.append(Spacer(1, 12))

    # Fechas
    fecha_factura = cotizacion.fecha.strftime("%d/%m/%Y")
    numero_factura = f"{cotizacion.id}"

    # Información del cliente y empresa (mejor diseño visual)
    cliente = [
        ["Nro de factura:", numero_factura],
        ["Fecha de factura:", fecha_factura],
        ["Nombre:", cotizacion.nombre],
        ["Email:", cotizacion.email],
    ]
    table_cliente = Table(cliente, colWidths=[150, 330])
    table_cliente.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0, colors.black),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.black),
        ('BACKGROUND', (0,0), (0,-1), colors.lightblue),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (0,0), (0,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(table_cliente)
    elements.append(Spacer(1, 20))



    # Tabla de productos
    headers = ["Descripción", "Unidades", "Precio Unitario", "Precio"]
    data = [
        [cotizacion.detalles, cotizacion.cantidad,
            f"{cotizacion.precio:.2f} $", f"{cotizacion.cantidad * cotizacion.precio:.2f} $"]
    ]
    data.insert(0, headers)

    tabla_productos = Table(data, colWidths=[200, 80, 100, 100])
    tabla_productos.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold')
    ]))
    elements.append(tabla_productos)
    elements.append(Spacer(1, 20))

        # Cálculos de totales
    subtotal = cotizacion.cantidad * cotizacion.precio
    iva = subtotal * Decimal("0.19")
    total = subtotal + iva

    # Tabla de totales
    totales = [
        ["Subtotal:", f"$ {subtotal:.2f}"],
        ["IVA (19%):", f"$ {iva:.2f}"],
        ["Total:", f"$ {total:.2f}"]
    ]
    tabla_totales = Table(totales, colWidths=[250, 100])
    tabla_totales.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('TEXTCOLOR', (0, 0), (0, -2), colors.black),
        ('TEXTCOLOR', (0, -1), (-1, 0), colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(tabla_totales)
    elements.append(Spacer(1, 20))

    # Generar PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer
