from django.core.management.base import BaseCommand, CommandParser

from food_calc.server.models import Product
from food_calc.server.util.scraper import BillaWebScraper


class Command(BaseCommand):
  help = 'Ingest product data'

  def add_arguments(self, parser: CommandParser):
    parser.add_argument('data_file')

  def handle(self, *args, **options):
    filename = options['data_file']
    scraper = BillaWebScraper()
    with open(filename) as file:
      for line in file:
        line = line.strip('\n')
        self.stdout.write('Processing "' + line + '"')
        ingredient = scraper.scrape_product(line)
        self.stdout.write('Finished product "' + ingredient.name + '"')
        ingredient.save()
