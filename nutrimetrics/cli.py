# SPDX-FileCopyrightText: 2023-present Thomas Civeit <thomas@civeit.com>
#
# SPDX-License-Identifier: MIT
"""Command Line Interface to run commands"""

import argparse
from pathlib import Path
import nutrimetrics.config as config
import pprint
from nutrimetrics.food_data_central import FoodDataCentral
from nutrimetrics.meals import load_foods, MealPlan
from nutrimetrics.workbook import WorkbookGenerator


def display_config():
    """Command that displays user's configuration."""
    pp = pprint.PrettyPrinter(indent=4, sort_dicts=False)
    pp.pprint(config.read_config())


def analyze_meal_plan():
    """Command that analyzes a meal plan."""
    parser = argparse.ArgumentParser(
        description='NutriMetrics - Analyze nutrients in a meal plan.',
        epilog=f"NutriMetrics configuration files live in '{config.config_dir}' directory."
    )
    parser.add_argument(
        'meal_plan.json',
        type=str,
        help='Path to meal plan JSON file to be processed'
    )
    args = parser.parse_args()
    json_file = Path(vars(args)['meal_plan.json'])
    if not json_file.exists():
        print(f"Data file '{json_file}' does not exist")
        exit()
    cfg = config.read_config()
    foods = load_foods()
    meal_plan = MealPlan(json_file, foods, cfg['dietary_reference_intakes'])
    generator = WorkbookGenerator(cfg['workbook_settings'], cfg['dietary_reference_intakes'])
    generator.generate(Path(json_file.name.replace('.json', '.xlsx')), meal_plan, foods)


def import_food_data_central():
    """Command that imports nutrient profile data from FoodData Central."""
    parser = argparse.ArgumentParser(
        description='NutriMetrics - Import food data from FoodData Central.',
        epilog=f"NutriMetrics configuration files live in '{config.config_dir}' directory."
    )
    parser.add_argument(
        'food_list.json',
        type=str,
        help='Path to food list JSON file to be processed'
    )
    args = parser.parse_args()
    json_file = Path(vars(args)['food_list.json'])
    if not json_file.exists():
        print(f"Data file '{json_file}' does not exist")
        exit()
    cfg = config.read_config()
    fdc = FoodDataCentral(
        cfg['food_data_central']['api_url'],
        cfg['food_data_central']['api_key'],
        cfg['food_data_central']['verbose_import'],
        cfg['food_data_central']['nutrients_ids']
    )
    fdc.import_food_list(json_file)
