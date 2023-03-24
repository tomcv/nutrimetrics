# NutriMetrics

NutriMetrics is a Python package that analyzes nutrients found in foods and user-defined meal plans.
Nutrient profile data can be imported from USDA's FoodData Central or manually entered by users.
The package tracks 60+ nutrients from the standard fats, proteins, and carbs to all minerals and vitamins.
It comes with 100+ nutrient profiles found in common raw food and a few sample meal plans.
User-defined meal plans consist of a set of meals, each of which consists of a set of foods
with a specified amount. Analysis reports are generated in Excel workbooks.

[![PyPI - Version](https://img.shields.io/pypi/v/nutrimetrics.svg)](https://pypi.org/project/nutrimetrics)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/nutrimetrics.svg)](https://pypi.org/project/nutrimetrics)

![Report Screenshot](report.png?raw=true)

-----

**Table of Contents**

- [Installation](#installation)
- [Quick Start Guide](#quick-start-guide)
- [License](#license)

## Installation

### PyPI

The easiest way to get NutriMetrics is to use pip:
```console
pip install nutrimetrics
```
That will install the `nutrimetrics` package along with all the required dependencies.
Pip will also install a few commands (described below) to the package's bin directory.

### From Source

Alternatively you can install the latest NutriMetrics codebase from the git repo:
```console
$ git clone https://github.com/tomcv/nutrimetrics.git
$ cd nutrimetrics
$ hatch build
```
The package's [pyproject.toml](pyproject.toml) project file is configured for [hatch](https://github.com/pypa/hatch).

## Quick Start Guide

The package includes 3 commands:

- `nutrimetrics-config` displays the current configuration
- `nutrimetrics-analyze` generates analysis report for a specified meal plan
- `nutrimetrics-import` imports nutrient profile data from USDA's FoodData Central

### Configuration

All configuration parameters are set in `~/.nutrimetrics/config.json`.
The default configuration is created if not found when running any commands.
The only parameter that you may have to change is the API key used to access FoodData Central
when importing data.

### Analysis Report

The package provides a sample meal plan you can use to run the `nutrimetrics-analyze` command:
```console
$ nutrimetrics-analyze ~/.nutrimetrics/samples/meal_plan.json 
```
Which will generate the corresponding `meal_plan.xlsx` Excel workbook in the working directory.
The report includes the amount of each nutrient as well as some statistical data,
including the energy distribution (i.e. percentage of fats, proteins and carbs)
and the percentage of the 'dietary reference intakes' for minerals and vitamins.
The first spreadsheet describes each meal of the meal plan, while the second spreadsheet
describes all known foods, defined in the `~/.nutrimetrics/foods/` directory. 

A meal plan is defined in a JSON file like this:
```json
{
  "name": "Simple Meal Plan",
  "unit": "g",
  "meals": [
    {
      "name": "Breakfast [7AM]",
      "foods": [
        {"food": "Oat Rolled", "amount": 40},
        {"food": "Blueberry", "amount": 80}
      ]
    },
    {
      "name": "Dinner [7PM]",
      "foods": [
        {"food": "Chicken Breast", "amount": 150},
        {"food": "Cauliflower", "amount": 100},
        {"food": "Olive Oil", "amount": 13}
      ]
    }
  ]
}
```
The `food` value must be one of the food's name defined in the `~/.nutrimetrics/foods/` directory.

### Nutrient Profile Data

The package comes with 100+ nutrient profiles of raw food. However, new data can be added by importing
nutrient profiles  from USDA's FoodData Central (FDC). The `nutrimetrics-import` command reads a JSON file
that lists all foods names and FDC IDs to be imported, looking like this:

```json
{
  "foods": [
    {"fdc_id": 170567,  "name": "Almond"},
    {"fdc_id": 170178,  "name": "Macadamia Nut"},
    {"fdc_id": 170187,  "name": "Walnut"}
  ]
}
```

The package provides a sample `~/.nutrimetrics/samples/foods.json` file you can use.
Before running the command you must edit `~/.nutrimetrics/config.json` to specify your own `api_key`
(that you can get it [here](https://fdc.nal.usda.gov/api-guide.html) for free).

```console
$ nutrimetrics-import ~/.nutrimetrics/samples/foods.json 
```
Will download and generate all JSON files in `~/.nutrimetrics/foods/` for each specified food.

Alternatively you can create your own JSON files by specifying the amount of each nutrient for a given food.
All amounts are specified in grams. Nutrients that are not listed are set to zero by default. 

## License

`nutrimetrics` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
