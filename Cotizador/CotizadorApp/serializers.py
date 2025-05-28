from rest_framework import serializers
from .models import Cotizacion, CustomUser, Categoria, Producto, DetalleFactura


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer para usuarios personalizados.
    Maneja creación y actualización incluyendo manejo de contraseñas.
    """
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'rut',
                  'telefono', 'email', 'username', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class CategoriaSerializer(serializers.ModelSerializer):
    """
    Serializer para la entidad Categoría.
    """
    class Meta:
        model = Categoria
        fields = ['id', 'nombre']


class ProductoSerializer(serializers.ModelSerializer):
    """
    Serializer para productos. Muestra datos de categoría como objeto anidado de solo lectura.
    """
    categoria = CategoriaSerializer(read_only=True)
    categoria_id = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.all(), source='categoria', write_only=True
    )

    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'descripcion', 'precio',
                  'stock', 'fecha_creacion', 'categoria', 'categoria_id']


class DetalleFacturaSerializer(serializers.ModelSerializer):
    """
    Serializer para los detalles de cotización (productos, cantidades y precios).
    """
    producto = ProductoSerializer(read_only=True)
    producto_id = serializers.PrimaryKeyRelatedField(
        queryset=Producto.objects.all(), source='producto', write_only=True
    )

    class Meta:
        model = DetalleFactura
        fields = ['id', 'producto', 'producto_id',
                  'cantidad', 'precio_unitario', 'precio_total']
        read_only_fields = ['precio_total']


class CotizacionSerializer(serializers.ModelSerializer):
    """
    Serializer para cotizaciones, incluyendo detalles anidados.
    """
    detalles = DetalleFacturaSerializer(many=True)

    class Meta:
        model = Cotizacion
        fields = ['id', 'user', 'fecha', 'detalles']
        read_only_fields = ['user']

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user
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
