from rest_framework import serializers

from food_calc.server.models import Product


# Serializers define the API representation.
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
