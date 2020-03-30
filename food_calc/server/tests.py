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
      product = self.scraper.scrape_product(product)
      self.assertIsNotNone(product.name)
      self.assertIsNotNone(product.calories)
      self.assertIsNotNone(product.nutrition_fat)
      self.assertIsNotNone(product.nutrition_carbohydrates)
      self.assertIsNotNone(product.nutrition_protein)
      product.save()

