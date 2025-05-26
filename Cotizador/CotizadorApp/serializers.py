from rest_framework import serializers
from .models import Cotizacion, CustomUser, Categoria, Producto, DetalleFactura

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'rut', 'telefono', 'email', 'username']

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre']

class ProductoSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer(read_only=True)
    categoria_id = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.all(), source='categoria', write_only=True
    )

    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'descripcion', 'precio', 'stock', 'fecha_creacion', 'categoria', 'categoria_id']

class DetalleFacturaSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer(read_only=True)
    producto_id = serializers.PrimaryKeyRelatedField(
        queryset=Producto.objects.all(), source='producto', write_only=True
    )

    class Meta:
        model = DetalleFactura
        fields = ['id', 'producto', 'producto_id', 'cantidad', 'precio_unitario', 'precio_total']
        read_only_fields = ['precio_total']

class CotizacionSerializer(serializers.ModelSerializer):
    detalles = DetalleFacturaSerializer(many=True)

    class Meta:
        model = Cotizacion
        fields = ['id', 'user', 'fecha', 'detalles']

    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles')
        cotizacion = Cotizacion.objects.create(**validated_data)
        for detalle in detalles_data:
            DetalleFactura.objects.create(cotizacion=cotizacion, **detalle)
        return cotizacion

    def update(self, instance, validated_data):
        detalles_data = validated_data.pop('detalles', [])
        instance = super().update(instance, validated_data)

        if detalles_data:
            instance.detalles.all().delete()
            for detalle in detalles_data:
                DetalleFactura.objects.create(cotizacion=instance, **detalle)
        return instance
