from django.db import models


class Ingredient(models.Model):
  name = models.CharField(max_length=255)
  shop = models.CharField(max_length=100, default='billa')
  item_number = models.CharField(max_length=100)

  # Price per 100g
  price = models.DecimalField(max_digits=10, decimal_places=6, null=True)
  # Kilocalories per 100g
  calories = models.PositiveIntegerField(default=0)
  # Macronutrition in percent
  macro_fat = models.DecimalField(max_digits=5, decimal_places=2, default=0)
  macro_fatty_acids = models.DecimalField(max_digits=5, decimal_places=2, default=0)
  macro_carbohydrates = models.DecimalField(max_digits=5, decimal_places=2, default=0)
  macro_sugar = models.DecimalField(max_digits=5, decimal_places=2, default=0)
  macro_protein = models.DecimalField(max_digits=5, decimal_places=2, default=0)
  macro_salt = models.DecimalField(max_digits=5, decimal_places=2, default=0)

  def __str__(self):
    return self.name
