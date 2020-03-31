# FoodCalculator
![Django CI](https://github.com/petritz/food-calculator/workflows/Django%20CI/badge.svg)

Tools for calculating recipe nutrition and cost. Including experiment creation for recipe development. Will be most useful for pastries or other baked goods.

## Setup
Setup virtual env:
```bash
$ virtualenv venv
$ . venv/bin/activate
$ pip install --upgrade pip
$ pip install -r requirements.txt
$ pip install -r dev_requirements.txt
```
Setup application:
```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

## Development
Run server:
```bash
$ python manage.py runserver
```

## Data
For now there is a connector to the Billa Onlineshop that fetches all needed information.