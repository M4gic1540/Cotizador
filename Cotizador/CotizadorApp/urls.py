from rest_framework.routers import DefaultRouter
from .views import CotizacionViewSet, UserViewSet, ProductoViewSet, CategoriaViewSet
from django.urls import path

router = DefaultRouter()
router.register(r'cotizaciones', CotizacionViewSet, basename='cotizacion')
router.register(r'usuarios', UserViewSet, basename='usuario')
router.register(r'productos', ProductoViewSet, basename='producto')
router.register(r'categorias', CategoriaViewSet, basename='categoria')
urlpatterns = router.urls
