from decimal import Decimal

import requests_mock
from django.db.models.base import Model
from django.test import TestCase
from django.utils.datetime_safe import date
from requests_mock import Mocker

from food_calc.server.models import IngredientType, Ingredient, Product, Recipe, Part, Details, Experiment, Variant
from food_calc.server.util.scraper import BillaWebScraper


class ExperimentCreationTestCase(TestCase):
    def test_can_create(self):
        type_flour = IngredientType.objects.create(name='flour')
        ingredient_wheat = Ingredient.objects.create(type=type_flour, characteristic='all-purpose wheat flour')
        product_flour = Product.objects.create(name='Henry Wheat Flour', ingredient=ingredient_wheat, shop='henry',
                                               item_number='001',
                                               price=Decimal('0.149'), calories=400)
        ingredient_wheat_whole = Ingredient.objects.create(type=type_flour, characteristic='whole wheat flour')
        product_whole_flour = Product.objects.create(name='Henry Whole Wheat Flour', ingredient=ingredient_wheat_whole,
                                                     shop='henry',
                                                     item_number='001',
                                                     price=Decimal('0.149'), calories=400)

        type_water = IngredientType.objects.create(name='water')
        ingredient_water = Ingredient.objects.create(type=type_water, characteristic='tap water')
        product_water = Product.objects.create(name='Austria Water', ingredient=ingredient_water, shop='austria',
                                               item_number='',
                                               price=Decimal('0.0002'), calories=0)

        bread_recipe = Recipe.objects.create(name='flat bread', description='easy ancient flat bread',
                                             serving_size=Decimal('50'))
        part = Part.objects.create(name='dough', ranking=1)
        Details.objects.create(recipe=bread_recipe, ingredient=ingredient_wheat, comment='room temperature',
                               amount=Decimal('150'), part=part)
        Details.objects.create(recipe=bread_recipe, ingredient=ingredient_water, comment='room temperature',
                               amount=Decimal('50'), part=part)

        bread_recipe2 = Recipe.objects.create(name='flat bread 2', description='easy ancient flat bread (with whole grain)',
                                              serving_size=Decimal('40'))
        Details.objects.create(recipe=bread_recipe2, ingredient=ingredient_wheat_whole,
                               comment='room temperature',
                               amount=Decimal('200'), part=part)
        Details.objects.create(recipe=bread_recipe2, ingredient=ingredient_water, comment='room temperature',
                               amount=Decimal('120'), part=part)

        experiment = Experiment.objects.create(name='Ancient Flatbread', test_date=date(830, 3, 12), test_size=Decimal('50'))
        # noinspection PyTypeChecker
        variant_1: Variant = Variant.objects.create(number='A', experiment=experiment, recipe=bread_recipe, part=part)
        variant_1.products.add(product_water)
        variant_1.products.add(product_flour)

        # noinspection PyTypeChecker
        variant_2: Variant = Variant.objects.create(number='B', experiment=experiment, recipe=bread_recipe, part=part)
        variant_2.products.add(product_water)
        variant_2.products.add(product_whole_flour)

        # noinspection PyTypeChecker
        variant_3: Variant = Variant.objects.create(number='C', experiment=experiment, recipe=bread_recipe2, part=part)
        variant_3.products.add(product_water)
        variant_3.products.add(product_whole_flour)


class BillaWebScrapingTestCase(TestCase):

    @requests_mock.Mocker()
    def test_can_process(self, mock: Mocker):
        scraper = BillaWebScraper()
        item_number = '00-12345'
        print('running: ' + item_number)

        base_json = """
        {
            "brand": "Markus Hof",
            "price": {
                "normal": 1.49,
                "sale": 1.49,
                "unit": null,
                "final": 1.49
            }
        }
        """

        info_json = """
        [
            {
                "name": "Frische Milch",
                "nutritions": [
                    {
                        "preperationGrade": "Unzubereitet für 100 Gramm",
                        "unit": "Gramm",
                        "relationValue": 100.0,
                        "nutritions": [
                            {
                                "nutritionName": "Energie",
                                "unit": "Kilojoule",
                                "nutritionalValue": 278.0
                            },
                            {
                                "nutritionName": "Energie",
                                "unit": "Kilokalorie",
                                "nutritionalValue": 67.0
                            },
                            {
                                "nutritionName": "Fett",
                                "unit": "Gramm",
                                "nutritionalValue": 3.8
                            },
                            {
                                "nutritionName": "   davon gesättigte Fettsäuren",
                                "unit": "Gramm",
                                "nutritionalValue": 2.3
                            },
                            {
                                "nutritionName": "Kohlenhydrate",
                                "unit": "Gramm",
                                "nutritionalValue": 4.8
                            },
                            {
                                "nutritionName": "   davon Zucker",
                                "unit": "Gramm",
                                "nutritionalValue": 4.8
                            },
                            {
                                "nutritionName": "Eiweiß",
                                "unit": "Gramm",
                                "nutritionalValue": 3.3
                            },
                            {
                                "nutritionName": "Salz",
                                "unit": "Gramm",
                                "nutritionalValue": 0.13
                            },
                            {
                                "nutritionName": "Kalzium",
                                "unit": "Milligramm",
                                "nutritionalValue": 120.0
                            }
                        ]
                    }
                ],
                "measurements": [
                    {
                        "type": "Bruttogewicht",
                        "value": 1.06,
                        "unit": "Kilogramm"
                    },
                    {
                        "type": "Nettogehalt",
                        "value": 1.0,
                        "unit": "Liter"
                    }
                ]
            }
        ]
        """

        mock.get(scraper.get_base_info_url(item_number), text=base_json)
        mock.get(scraper.get_info_url(item_number), text=info_json)

        product = scraper.scrape_product(item_number)
        assert product.name == "Markus Hof Frische Milch"
        assert product.calories == Decimal('67')
        assert product.nutrition_fat == Decimal('3.8')
        assert product.nutrition_carbohydrates == Decimal('4.8')
        assert product.nutrition_protein == Decimal('3.3')
        assert product.price == (Decimal('1.49') / (Decimal('1000') * Decimal('1.03'))) * Decimal('100')

        print('processed: ' + item_number)
        product.save()
        print('saved: ' + item_number)
