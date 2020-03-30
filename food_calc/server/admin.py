from django.contrib import admin

# Register your models here.
from food_calc.server.models import Product

admin.site.register(Product)
