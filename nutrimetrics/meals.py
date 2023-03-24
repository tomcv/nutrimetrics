# SPDX-FileCopyrightText: 2023-present Thomas Civeit <thomas@civeit.com>
#
# SPDX-License-Identifier: MIT
"""Defines food, meal, and meal plan."""

from nutrimetrics.nutrients import nutrients_list, EnergyDistribution
from jsmin import jsmin
import json
import os
from pathlib import Path
import nutrimetrics.config as config
import copy
from collections import OrderedDict
from nutrimetrics.units import convert_amount


class Food:
    """Defines food that consists of nutrients."""
    def __init__(self, name='', amount=0):
        self.name = name
        self.amount = amount
        self.nutrients = dict()  # key: nutrient's data_name, value: amount
        for nutrient in nutrients_list:
            self.nutrients[nutrient.data_name] = 0  # nutrient amount is zero by default

    def to_json(self, indent):
        return json.dumps(self, default=lambda obj: obj.__dict__, indent=indent)

    @staticmethod
    def from_json(json_file):
        data = json.loads(jsmin(json_file.read()))
        food = Food()
        food.name = data['name']
        food.amount = data['amount']
        for ntr, amt in data['nutrients'].items():
            food.nutrients[ntr] = amt
        return food

    def multiply(self, m):
        self.amount *= m
        for nutrient in nutrients_list:
            self.nutrients[nutrient.data_name] *= m

    def add(self, other_food):
        self.amount += other_food.amount
        for nutrient in nutrients_list:
            self.nutrients[nutrient.data_name] += other_food.nutrients[nutrient.data_name]


class FoodTotal(Food):
    """A food total is used to store combined foods."""
    def __init__(self, name):
        super().__init__(name=name, amount=0)


def load_foods():
    """Load all foods defined in dedicated configuration directory."""
    foods = dict()
    for file in [Path(f) for f in os.listdir(config.foods_dir)]:
        if file.suffix == '.json':
            with open(Path(config.foods_dir, file), 'r') as json_file:
                food = Food.from_json(json_file)
                foods[food.name] = food
    return OrderedDict(sorted(foods.items()))


class Meal:
    """Defines meal that consists of foods."""
    def __init__(self, unit, data, foods_dict):
        self.name = data["name"]
        self.foods = []
        for data_food in data["foods"]:
            food_name = data_food["food"]
            if food_name not in foods_dict:
                print(f"ERROR: food '{food_name}' is unknown")
            else:
                food = copy.deepcopy(foods_dict[food_name])  # do not modify object in dict
                amount = convert_amount(data_food["amount"], unit)
                food.multiply(amount / food.amount)
                self.foods.append(food)
        # calculate total nutrients
        self.total = FoodTotal(name='TOTAL')
        for food in self.foods:
            self.total.add(food)


class MealPlan:
    """Defines meal plan that consists of meals."""
    def __init__(self, json_file, foods_dict, dri_dict):
        with open(json_file, 'r') as file:
            data = json.loads(jsmin(file.read()))
        self.name = data["name"]
        self.unit = data["unit"]
        self.meals = []
        for meal_data in data["meals"]:
            self.meals.append(Meal(self.unit, meal_data, foods_dict))
        # calculate total nutrients
        self.total = FoodTotal(name='GRAND TOTAL')
        for meal in self.meals:
            self.total.add(meal.total)
        # calculate energy distribution
        self.distribution = EnergyDistribution(self.total.nutrients["protein"],
                                               self.total.nutrients["carbohydrate"],
                                               self.total.nutrients["fat"])
        # calculate DRI ratio
        self.dri_ratio = dict()  # key: nutrient's data_name, value: DRI ratio
        for ntr_name in [nutrient.data_name for nutrient in nutrients_list]:
            if ntr_name in dri_dict:
                self.dri_ratio[ntr_name] = self.total.nutrients[ntr_name] / dri_dict[ntr_name]
