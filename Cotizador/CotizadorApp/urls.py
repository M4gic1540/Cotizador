from rest_framework.routers import DefaultRouter
from .views import CotizacionViewSet, UserViewSet
from django.urls import path

router = DefaultRouter()
router.register(r'cotizaciones', CotizacionViewSet, basename='cotizacion')
router.register(r'usuarios', UserViewSet, basename='usuario')

urlpatterns = router.urls
