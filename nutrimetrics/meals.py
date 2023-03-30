# SPDX-FileCopyrightText: 2023-present Thomas Civeit <thomas@civeit.com>
#
# SPDX-License-Identifier: MIT
"""Defines food, meal, and meal plan."""

from nutrimetrics.nutrients import nutrients_list
import json
import os
from pathlib import Path
import nutrimetrics.config as config
import copy
from collections import OrderedDict
from nutrimetrics.units import convert_amount


energy_protein_factor = 4
energy_carbohydrate_factor = 4
energy_fat_factor = 8


class Food:
    """Defines food that consists of nutrients."""
    def __init__(self, name='', description='', amount=0):
        self.name = name
        self.description = description
        self.amount = amount
        self.nutrients = dict()  # key: nutrient's data_name, value: amount
        for nutrient in nutrients_list:
            self.nutrients[nutrient.data_name] = 0  # nutrient amount is zero by default

    def to_json(self, indent):
        return json.dumps(self, default=lambda obj: obj.__dict__, indent=indent)

    @staticmethod
    def from_json(json_file):
        data = config.read_json(json_file)
        food = Food()
        if data:
            food.name = data['name']
            food.description = data['description']
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
        super().__init__(name=name, description='', amount=0)


def load_foods():
    """Load all foods defined in dedicated configuration directory."""
    foods = dict()
    for file in [Path(f) for f in os.listdir(config.foods_dir)]:
        if file.suffix == '.json':
            food = Food.from_json(Path(config.foods_dir, file))
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
    def __init__(self, data, foods_dict):
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
        # load DRI
        self.dri_name = data["dietary_reference_intakes"]
        self.dri_dict = self.load_dietary_reference_intakes()
        # calculate target
        self.target = Target(
            convert_amount(data["target"]["body_mass"], self.unit),
            data["target"]["body_fat_percent"] / 100,
            data["target"]["activity_factor"],
            data["target"]["minimum_protein_factor"],
            data["target"]["minimum_fat_factor"],
        )
        # add target to DRI
        self.dri_dict['energy'] = self.target.basal_metabolic_rate
        self.dri_dict['protein'] = self.target.minimum_protein
        self.dri_dict['fat'] = self.target.minimum_fat
        # calculate DRI ratio
        self.dri_ratio = dict()  # key: nutrient's data_name, value: DRI ratio
        for ntr_name in [nutrient.data_name for nutrient in nutrients_list]:
            if ntr_name in self.dri_dict:
                self.dri_ratio[ntr_name] = self.total.nutrients[ntr_name] / self.dri_dict[ntr_name]

    def load_dietary_reference_intakes(self):
        dri_file = Path(config.dri_dir, f'{self.dri_name}.json')
        if not dri_file.exists():
            print(f"ERROR: DRI file '{dri_file.absolute()}' does not exist")
            return dict()
        data = config.read_json(dri_file)
        return data['dietary_reference_intakes'] if data else dict()


class Target:
    def __init__(self, body_mass, body_fat_ratio, activity_factor, minimum_protein_factor, minimum_fat_factor):
        self.body_mass = body_mass
        self.body_fat_ratio = body_fat_ratio
        self.activity_factor = activity_factor
        self.minimum_protein_factor = minimum_protein_factor
        self.minimum_fat_factor = minimum_fat_factor
        # calculate derived variables
        self.lean_body_mass = (1 - self.body_fat_ratio) * self.body_mass
        # Katch–McArdle formula: Resting Daily Energy Expenditure (RDEE)
        self.resting_energy = 370 + (21.6 * (self.lean_body_mass / 1000))
        self.basal_metabolic_rate = self.resting_energy * self.activity_factor
        self.minimum_protein = self.lean_body_mass * self.minimum_protein_factor / 1000  # kg to g
        self.minimum_fat = self.lean_body_mass * self.minimum_fat_factor / 1000  # kg to g


class EnergyDistribution:
    """Defines an energy distribution in fats, proteins and carbs."""
    def __init__(self, protein_amount, carb_amount, fat_amount):
        self.energy_protein = protein_amount * energy_protein_factor
        self.energy_carb = carb_amount * energy_carbohydrate_factor
        self.energy_fat = fat_amount * energy_fat_factor
        self.energy_total = self.energy_protein + self.energy_carb + self.energy_fat
        self.protein_ratio = self.energy_protein / self.energy_total
        self.carbohydrate_ratio = self.energy_carb / self.energy_total
        self.fat_ratio = self.energy_fat / self.energy_total
