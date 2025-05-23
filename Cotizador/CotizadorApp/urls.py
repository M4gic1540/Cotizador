from rest_framework.routers import DefaultRouter
from .views import CotizacionViewSet
from .views import DescargarPDFView
from django.urls import path

router = DefaultRouter()
router.register(r'cotizaciones', CotizacionViewSet, basename='cotizacion')

urlpatterns = router.urls

urlpatterns = [
    # ... otras rutas
    path('cotizaciones/<int:pk>/pdf/', DescargarPDFView.as_view(), name='cotizacion-pdf'),
]