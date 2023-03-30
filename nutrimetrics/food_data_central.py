# SPDX-FileCopyrightText: 2023-present Thomas Civeit <thomas@civeit.com>
#
# SPDX-License-Identifier: MIT
"""Defines the FoodData Central interface to import data."""

import json
import requests
import nutrimetrics.config as config
from pathlib import Path
from nutrimetrics.meals import Food
from nutrimetrics.units import convert_amount


class FoodDataCentral:
    """Defines the FoodData Central interface to import data."""
    def __init__(self, api_url, api_key, verbose_import, nutrients_ids, replace_existing):
        self.api_url = api_url
        self.api_key = api_key
        self.verbose_import = verbose_import
        self.nutrients_ids = nutrients_ids
        self.replace_existing = replace_existing
        self.session = None

    def import_food_list(self, data):
        self.session = requests.Session()
        for food in data['foods']:
            food_name, fdc_id = food['name'], food['fdc_id']
            food_file = Path(config.foods_dir, food_name.lower().replace(' ', '_') + f'_{fdc_id}.json')
            if food_file.exists() and not self.replace_existing:
                print(f"> Do not import {food_name}: {food_file.absolute()} already exists")
                continue
            fdc_data = self.download(fdc_id, food_name)
            if fdc_data:
                self.write_food_file(fdc_id, food_name, food_file, fdc_data)

    def download(self, fdc_id, food_name):
        query = f'{self.api_url}/food/{fdc_id}?api_key={self.api_key}'
        print(f'Fetching {food_name} ({fdc_id}) GET {query}')
        res = self.session.get(query)
        if res.status_code != 200:
            print(f'ERROR: FoodData Central return status={res.status_code}')
            return None
        else:
            return json.loads(res.content.decode())

    def get_nutrient_data_name(self, ntr_id):
        for nutrient_name, nutrient_ids in self.nutrients_ids.items():
            if ntr_id in nutrient_ids:
                return nutrient_name
        return None

    def write_food_file(self, fdc_id, food_name, food_file, fdc_data):
        # FoodData Central nutrients are always provided for 100 grams
        food = Food(food_name, fdc_data['description'], amount=100)
        for food_nutrient in fdc_data["foodNutrients"]:
            if "amount" in food_nutrient:
                ntr_id = food_nutrient["nutrient"]["id"]
                ntr_unit = food_nutrient["nutrient"]["unitName"]
                ntr_amount = food_nutrient["amount"]
                ntr_name = food_nutrient["nutrient"]["name"]
                data_name = self.get_nutrient_data_name(ntr_id)
                if self.verbose_import:
                    verbose = f'{food_name} ({fdc_id}): [{ntr_name}][{ntr_id}][{ntr_amount}][{ntr_unit}]'
                    verbose += f' -> {data_name}' if data_name else ''
                    print(verbose)
                if data_name:
                    food.nutrients[data_name] = convert_amount(ntr_amount, ntr_unit)
        with open(food_file, 'w') as file:
            file.write(food.to_json(indent=2))
        print(f'> Imported to {food_file.absolute()}')
