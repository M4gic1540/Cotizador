from rest_framework.routers import DefaultRouter
from .views import CotizacionViewSet
from django.urls import path

router = DefaultRouter()
router.register(r'cotizaciones', CotizacionViewSet, basename='cotizacion')

urlpatterns = router.urls
