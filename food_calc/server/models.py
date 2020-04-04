from django.db import models


class IngredientType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    type = models.ForeignKey(IngredientType, on_delete=models.CASCADE)
    characteristic = models.CharField(max_length=500)

    def __str__(self):
        return self.type.name + ", " + self.characteristic


class Product(models.Model):
    name = models.CharField(max_length=255)
    ingredient = models.ForeignKey(Ingredient, null=True, on_delete=models.CASCADE)
    shop = models.CharField(max_length=100, default='billa')
    item_number = models.CharField(max_length=100)

    # Price per 100g
    price = models.DecimalField(max_digits=10, decimal_places=4, null=True)
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


class Recipe(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    serving_size = models.DecimalField(max_digits=6, decimal_places=2)
    ingredients = models.ManyToManyField(Ingredient, through='Details')

    def __str__(self):
        return self.name


class Part(models.Model):
    name = models.CharField(max_length=255)
    # Determines the order, e.g. a dough is definitely more important than the filling
    ranking = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Details(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    comment = models.TextField()
    # Amount is always saved in gram
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    part = models.ForeignKey(Part, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.amount) + " " + self.ingredient.type.name + " (" + self.recipe.name + ")"


class Experiment(models.Model):
    name = models.CharField(max_length=255)
    test_date = models.DateField()
    test_size = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name


class Variant(models.Model):
    # Number in Experiment
    number = models.CharField(max_length=100)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    # If this is set, then only use the specified part from the recipe, disregarding the rest
    part = models.ForeignKey(Part, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.experiment.name + " " + self.number
