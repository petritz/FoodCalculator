from decimal import Decimal

from food_calc.server.models import Product
import requests
import json


class WebScraper:
    def get_name(self):
        raise NotImplementedError()

    def scrape_product(self, item_number: str) -> Product:
        raise NotImplementedError()


class BillaWebScraper(WebScraper):
    api_url = 'https://www.billa.at/api/articles/'

    def get_name(self):
        return 'billa'

    def scrape_product(self, item_number: str) -> Product:
        ingredient = Product()
        ingredient.item_number = item_number
        ingredient.shop = self.get_name()

        price = None
        brand = ''
        base_response = requests.get(self.api_url + item_number + "?includeDetails=true")
        if base_response.status_code == 200:
            # Can be non-200 if item is not currently available
            base_decoded = json.loads(base_response.text)
            price = Decimal(str(base_decoded['price']['final']))
            brand = base_decoded['brand']

        info_response = requests.get(self.api_url + item_number + "/infos")
        if info_response.status_code == 200:
            info_decoded = json.loads(info_response.text)[-1]

            # Weight in gramm
            weight = self.find_weight(info_decoded)
            nutrition = self.find_nutrition(info_decoded)

            ingredient.name = brand + " " + info_decoded['name']
            if price is not None and weight != 0:
                ingredient.price = (price / weight) * 100  # price per 100g
            ingredient.calories = nutrition.get('Energie')
            ingredient.nutrition_fat = nutrition.get('Fett')
            ingredient.nutrition_saturated_fatty_acids = nutrition.get('   davon gesättigte Fettsäuren')
            ingredient.nutrition_carbohydrates = nutrition.get('Kohlenhydrate')
            ingredient.nutrition_sugar = nutrition.get('   davon Zucker')
            ingredient.nutrition_protein = nutrition.get('Eiweiß')
            ingredient.nutrition_salt = nutrition.get('Salz')
            ingredient.nutrition_fiber = nutrition.get('Ballaststoffe')
            ingredient.nutrition_mono_unsaturated_fatty_acids = nutrition.get('   davon einfach ungesättigte Fettsäuren')
            ingredient.nutrition_poly_unsaturated_fatty_acids = nutrition.get('   davon mehrfach ungesättigte Fettsäuren')
            ingredient.nutrition_calcium = nutrition.get('Kalzium')
            ingredient.nutrition_calcium = nutrition.get('Natrium')

        return ingredient

    def find_nutrition(self, info_decoded):
        nutrition = {}
        for item in info_decoded['nutritions']:
            if item['unit'] == 'Gramm' and item['relationValue'] == 100 and len(nutrition) == 0:
                for nutri in item['nutritions']:
                    if nutri['unit'] == 'Kilokalorie' or nutri['unit'] == 'Gramm' or nutri['unit'] == 'Milligramm':
                        nutrition[nutri['nutritionName']] = Decimal(str(nutri['nutritionalValue']))
                        if nutri['unit'] == 'Milligramm':
                            nutrition[nutri['nutritionName']] /= 1000
        return nutrition

    def find_weight(self, info_decoded):
        for item in info_decoded['measurements']:
            if item['type'] == 'Nettogehalt':
                return self.calc_weight(info_decoded, item)
        return 0

    def calc_weight(self, info_decoded, item):
        weight = 0
        if item['unit'] == 'Gramm':
            weight = Decimal(str(item['value']))
        elif item['unit'] == 'Kilogramm':
            weight = Decimal(str(item['value'])) * 1000
        elif item['unit'] == 'Liter' or item['unit'] == 'Milliliter':
            # Assuming water
            weight = Decimal(str(item['value']))
            if item['unit'] == 'Liter':
                weight *= 1000

            if "Milch" in str(info_decoded['name']):
                weight *= 1.03
            elif "Öl" in str(info_decoded['name']):
                weight *= 0.8
        elif item['unit'] == 'Stueck':
            portion = [x for x in info_decoded['measurements'] if x['type'] == 'Portionsgroesse']
            if portion:
                weight = Decimal(str(portion[0]['value'])) * Decimal(str(item['value']))
        return weight
