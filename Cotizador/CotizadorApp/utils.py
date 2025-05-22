#from io import BytesIO
#from reportlab.pdfgen import canvas
#from django.core.mail import EmailMessage
#from django.template.loader import render_to_string
#
#def generar_pdf_y_enviar_email(cotizacion):
#    buffer = BytesIO()
#    p = canvas.Canvas(buffer)
#    p.drawString(100, 800, f"Cotización para {cotizacion.nombre}")
#    p.drawString(100, 780, f"Detalles: {cotizacion.detalles}")
#    p.drawString(100, 760, f"Cantidad: {cotizacion.cantidad}")
#    p.drawString(100, 740, f"Precio: ${cotizacion.precio}")
#    p.drawString(100, 720, f"Fecha: {cotizacion.fecha.strftime('%Y-%m-%d')}")
#    p.showPage()
#    p.save()
#    buffer.seek(0)
#    email = EmailMessage(
#        'Su Cotización',
#        'Adjunto encontrará su cotización en PDF.',
#        'from@example.com',
#        [cotizacion.email],
#    )
#    email.attach('cotizacion.pdf', buffer.read(), 'application/pdf')
#    email.send()
#    buffer.close()
#    return True