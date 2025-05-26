from io import BytesIO
from decimal import Decimal
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    Table, TableStyle, SimpleDocTemplate, Paragraph, Spacer
)
from reportlab.lib.styles import getSampleStyleSheet


def generar_pdf(cotizacion):
    """
    Genera un archivo PDF con una factura a partir del objeto `cotizacion`.

    Args:
        cotizacion: Objeto con los atributos necesarios como `id`, `fecha`,
                    `nombre`, `email`, `detalles`, `cantidad`, `precio`.

    Returns:
        BytesIO: Contenido del PDF generado en un buffer en memoria.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # Secciones del PDF
    elements.append(Paragraph("<b>Factura</b>", styles['Title']))
    elements.append(Spacer(1, 12))

    elements.append(_crear_tabla_cliente(cotizacion))
    elements.append(Spacer(1, 20))

    elements.append(_crear_tabla_productos(cotizacion))
    elements.append(Spacer(1, 20))

    elements.append(_crear_tabla_totales(cotizacion))
    elements.append(Spacer(1, 20))

    doc.build(elements)
    buffer.seek(0)
    return buffer


def _crear_tabla_cliente(cotizacion):
    datos = [
        ["Nro de factura:", str(cotizacion.id)],
        ["Fecha de factura:", cotizacion.fecha.strftime("%d/%m/%Y")],
        ["Nombre:", cotizacion.user.first_name + " " + cotizacion.user.last_name],
        ["Email:", cotizacion.user.email],
        ["Teléfono:", cotizacion.user.telefono],
        ["RUT:", cotizacion.user.rut]
    ]
    tabla = Table(datos, colWidths=[150, 330])
    tabla.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 0, colors.black),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('BACKGROUND', (0, 0), (0, -1), colors.lightblue),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
    ]))
    return tabla


def _crear_tabla_productos(cotizacion):
    """
    Crea una tabla con los productos y precios.

    Returns:
        Table: Tabla con la descripción del producto.
    """
    headers = ["Descripción", "Unidades", "Precio Unitario", "Precio Total"]
    precio_unitario = cotizacion.precio
    cantidad = cotizacion.cantidad
    precio_total = cantidad * precio_unitario

    filas = [
        headers,
        [
            cotizacion.detalles,
            cantidad,
            f"$ {precio_unitario}",
            f"$ {precio_total}"
        ]
    ]

    tabla = Table(filas, colWidths=[200, 80, 100, 100])
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold')
    ]))
    return tabla


def _crear_tabla_totales(cotizacion):
    """
    Calcula los totales e IVA, y retorna una tabla con esta información.

    Returns:
        Table: Tabla de totales (subtotal, IVA, total).
    """
    cantidad = cotizacion.cantidad
    precio = cotizacion.precio
    subtotal = cantidad * precio
    iva = subtotal * Decimal("0.19")
    total = subtotal + iva

    datos_totales = [
        ["Subtotal:", f"$ {subtotal:.2f}"],
        ["IVA (19%):", f"$ {iva:.2f}"],
        ["Total:", f"$ {total:.2f}"]
    ]

    tabla = Table(datos_totales, colWidths=[250, 100])
    tabla.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('TEXTCOLOR', (0, 0), (0, -2), colors.black),
        ('TEXTCOLOR', (0, -1), (-1, 0), colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
    ]))
    return tabla
