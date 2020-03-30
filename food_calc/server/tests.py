from django.test import TestCase

from food_calc.server.util.scraper import BillaWebScraper


class BillaWebScrapingTestCase(TestCase):
  products = []
  scraper = None

  def setUp(self):
    self.scraper = BillaWebScraper()
    with open('sample_data.txt') as file:
      self.products = [x.strip('\n') for x in file.readlines()]

  def test_can_process(self):
    for product in self.products:
      ingredient = self.scraper.scrape_product(product)
      self.assertIsNotNone(ingredient.name)
      self.assertIsNotNone(ingredient.calories)
      self.assertIsNotNone(ingredient.macro_fat)
      self.assertIsNotNone(ingredient.macro_carbohydrates)
      self.assertIsNotNone(ingredient.macro_protein)
      ingredient.save()

