# FoodCalculator
![Django CI](https://github.com/petritz/food-calculator/workflows/Django%20CI/badge.svg)

Calculate price, calories, etc of recipes

## Setup
1. Setup virtual env:
```bash
$ virtualenv venv
$ . venv/bin/activate
$ pip install --upgrade pip
$ pip install -r requirements.txt
$ pip install -r dev_requirements.txt
```
1. Setup application:
```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

## Development
Run server:
```bash
$ python manage.py runserver
```
