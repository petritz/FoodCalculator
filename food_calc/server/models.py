from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    shop = models.CharField(max_length=100, default='billa')
    item_number = models.CharField(max_length=100)

    # Price per 100g
    price = models.DecimalField(max_digits=10, decimal_places=6, null=True)
    # Kilocalories per 100g
    calories = models.PositiveIntegerField(default=0)
    # Nutrition in percent
    nutrition_fat = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    nutrition_saturated_fatty_acids = models.DecimalField(max_digits=5, decimal_places=2, default=0, null=True)
    nutrition_carbohydrates = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    nutrition_sugar = models.DecimalField(max_digits=5, decimal_places=2, default=0, null=True)
    nutrition_protein = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    nutrition_salt = models.DecimalField(max_digits=5, decimal_places=2, default=0, null=True)
    nutrition_fiber = models.DecimalField(max_digits=5, decimal_places=2, default=0, null=True)
    nutrition_mono_unsaturated_fatty_acids = models.DecimalField(max_digits=5, decimal_places=2, default=0, null=True)
    nutrition_poly_unsaturated_fatty_acids = models.DecimalField(max_digits=5, decimal_places=2, default=0, null=True)
    nutrition_calcium = models.DecimalField(max_digits=7, decimal_places=4, default=0, null=True)
    nutrition_natrium = models.DecimalField(max_digits=7, decimal_places=4, default=0, null=True)

    def __str__(self):
        return self.name
