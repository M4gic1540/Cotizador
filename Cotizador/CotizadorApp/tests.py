import os
from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Cotizacion
from django.utils import timezone
from datetime import timedelta

if not settings.configured:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Cotizador.settings')
    settings.configure()


class CotizacionTests(APITestCase):
    def setUp(self):
        self.cotizacion_data = {
            'nombre': 'Test Nombre',
            'email': 'test@example.com',
            'detalles': 'Test Detalles',
            'cantidad': 10,
            'precio': 100.00,
            'fecha': timezone.now()
        }
        self.cotizacion = Cotizacion.objects.create(**self.cotizacion_data)

    def test_create_cotizacion(self):
        """
        Verifica que se pueda crear una cotización correctamente.
        """
        url = reverse('cotizacion-list')
        response = self.client.post(url, self.cotizacion_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cotizacion.objects.count(), 2)
        self.assertEqual(Cotizacion.objects.last().nombre,
                         self.cotizacion_data['nombre'])

    def test_list_cotizaciones(self):
        """
        Verifica que se pueda obtener la lista de cotizaciones.
        """
        url = reverse('cotizacion-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['nombre'],
                         self.cotizacion_data['nombre'])

    def test_update_cotizacion(self):
        """
        Verifica que se pueda actualizar una cotización existente.
        """
        updated_data = {
            'nombre': 'Updated Nombre',
            'email': 'updated@example.com',
            'detalles': 'Updated Detalles',
            'cantidad': 20,
            'precio': 200.00
        }
        url = reverse('cotizacion-detail', kwargs={'pk': self.cotizacion.id})
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.cotizacion.refresh_from_db()
        self.assertEqual(self.cotizacion.nombre, updated_data['nombre'])

    def test_delete_cotizacion(self):
        """
        Verifica que se pueda eliminar una cotización correctamente.
        """
        url = reverse('cotizacion-detail', kwargs={'pk': self.cotizacion.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Cotizacion.objects.count(), 0)

    def test_descargar_pdf(self):
        """
        Verifica que se pueda descargar el PDF de la cotización.
        """
        url = reverse('cotizacion-descargar-pdf', kwargs={'pk': self.cotizacion.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertEqual(response['Content-Disposition'],
                         f'attachment; filename="cotizacion_{self.cotizacion.id}.pdf"')

    def test_filter_by_email(self):
        """
        Verifica que el filtrado por email funcione correctamente.
        """
        response = self.client.get(
            reverse('cotizacion-list'), {'email': self.cotizacion.email})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['email'], self.cotizacion.email)

    def test_search_by_detalles(self):
        """
        Verifica que la búsqueda en el campo 'detalles' funcione correctamente.
        """
        response = self.client.get(
            reverse('cotizacion-list'), {'search': 'Test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
        self.assertIn('Test', response.data[0]['detalles'])

    def test_filter_by_date_range(self):
        """
        Verifica que el filtro por rango de fechas funcione correctamente.
        """
        # Cotización con fecha de ayer
        ayer = timezone.now() - timedelta(days=1)
        Cotizacion.objects.create(
            nombre='Pasado',
            email='past@example.com',
            detalles='Vieja cotización',
            cantidad=1,
            precio=1.00,
            fecha=ayer
        )
        # Filtro desde hoy en adelante (debería excluir la de ayer)
        response = self.client.get(
            reverse('cotizacion-list'), {'start_date': timezone.now().date().isoformat()})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(all(item['fecha'] >= timezone.now(
        ).date().isoformat() for item in response.data))
