from decimal import Decimal

import requests_mock
from django.test import TestCase
from requests_mock import Mocker

from food_calc.server.util.scraper import BillaWebScraper


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
