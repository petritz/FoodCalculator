from rest_framework import viewsets
from food_calc.server.models import Product
from food_calc.server.serializers import ProductSerializer


# ViewSets define the view behavior.
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
