# SPDX-FileCopyrightText: 2023-present Thomas Civeit <thomas@civeit.com>
#
# SPDX-License-Identifier: MIT
"""Defines nutrient profile data."""

from nutrimetrics.units import unit_kcal, unit_gram, unit_milligram, unit_microgram


class Nutrient:
    """Defines a nutrient."""
    def __init__(self, data_name, display_name, display_unit):
        self.data_name = data_name
        self.display_name = display_name
        self.display_unit = display_unit


nutrients_list = [
    Nutrient('energy', 'Energy', unit_kcal),
    Nutrient('water', 'Water', unit_gram),
    Nutrient('fat', 'Fat', unit_gram),
    Nutrient('mono-unsaturated', 'MonoUnsaturated', unit_gram),
    Nutrient('poly-unsaturated', 'PolyUnsaturated', unit_gram),
    Nutrient('saturated', 'Saturated', unit_gram),
    Nutrient('trans', 'Trans', unit_gram),
    Nutrient('cholesterol', 'Cholesterol', unit_milligram),
    Nutrient('protein', 'Protein', unit_gram),
    Nutrient('carbohydrate', 'Carbohydrate', unit_gram),
    Nutrient('fiber', 'Fiber', unit_gram),
    Nutrient('sugar', 'Sugar', unit_gram),
    Nutrient('starch', 'Starch', unit_gram),
    Nutrient('sucrose', 'Sucrose', unit_gram),
    Nutrient('glucose', 'Glucose', unit_gram),
    Nutrient('fructose', 'Fructose', unit_gram),
    Nutrient('lactose', 'Lactose', unit_gram),
    Nutrient('maltose', 'Maltose', unit_gram),
    Nutrient('galactose', 'Galactose', unit_gram),
    # minerals
    Nutrient('calcium', 'Calcium', unit_milligram),
    Nutrient('copper', 'Copper', unit_microgram),
    Nutrient('iron', 'Iron', unit_milligram),
    Nutrient('magnesium', 'Magnesium', unit_milligram),
    Nutrient('manganese', 'Manganese', unit_milligram),
    Nutrient('molybdenum', 'Molybdenum', unit_microgram),
    Nutrient('phosphorus', 'Phosphorus', unit_milligram),
    Nutrient('potassium', 'Potassium', unit_milligram),
    Nutrient('selenium', 'Selenium', unit_microgram),
    Nutrient('sodium', 'Sodium', unit_milligram),
    Nutrient('zinc', 'Zinc', unit_milligram),
    # vitamins
    Nutrient('vitamin-a', 'Vitamin A', unit_microgram),
    Nutrient('retinol', 'Retinol (A1)', unit_microgram),
    Nutrient('thiamin', 'Thiamin (B1)', unit_milligram),
    Nutrient('riboflavin', 'Riboflavin (B2)', unit_milligram),
    Nutrient('niacin', 'Niacin (B3)', unit_milligram),
    Nutrient('pantothenic-acid', 'Pantothenic Acid (B5)', unit_milligram),
    Nutrient('vitamin-b6', 'Vitamin B6', unit_milligram),
    Nutrient('biotin', 'Biotin (B7)', unit_microgram),
    Nutrient('folate', 'Folate (B9)', unit_microgram),
    Nutrient('folic-acid', 'Folic Acid', unit_microgram),
    Nutrient('vitamin-b12', 'Vitamin B12', unit_microgram),
    Nutrient('choline', 'Choline', unit_milligram),
    Nutrient('vitamin-c', 'Vitamin C', unit_milligram),
    Nutrient('vitamin-d', 'Vitamin D', unit_microgram),
    Nutrient('vitamin-e', 'Vitamin E', unit_milligram),
    Nutrient('phylloquinone', 'Phylloquinone (K1)', unit_microgram),
    Nutrient('menaquinone', 'Menaquinone (K2)', unit_microgram),
    # essential amino acids
    Nutrient('histidine', 'Histidine', unit_milligram),
    Nutrient('isoleucine', 'Isoleucine', unit_milligram),
    Nutrient('leucine', 'Leucine', unit_milligram),
    Nutrient('lysine', 'Lysine', unit_milligram),
    Nutrient('methionine', 'Methionine', unit_milligram),
    Nutrient('phenylalanine', 'Phenylalanine', unit_milligram),
    Nutrient('threonine', 'Threonine', unit_milligram),
    Nutrient('tryptophan', 'Tryptophan', unit_milligram),
    Nutrient('valine', 'Valine', unit_milligram),
    # non-essential amino acids
    Nutrient('arginine', 'Arginine', unit_milligram),
    Nutrient('cystine', 'Cystine', unit_milligram),
    Nutrient('glycine', 'Glycine', unit_milligram),
    Nutrient('proline', 'Proline', unit_milligram),
    Nutrient('tyrosine', 'Tyrosine', unit_milligram),
    Nutrient('alanine', 'Alanine', unit_milligram),
    Nutrient('aspartic-acid', 'Aspartic Acid', unit_milligram),
    Nutrient('glutamic-acid', 'Glutamic Acid', unit_milligram),
    Nutrient('serine', 'Serine', unit_milligram),
    Nutrient('hydroxyproline', 'Hydroxyproline', unit_milligram),
    # alkaloids
    Nutrient('caffeine', 'Caffeine', unit_milligram),
    Nutrient('theobromine', 'Theobromine', unit_milligram),
]

nutrients_dict = dict()
for nutrient in nutrients_list:
    nutrients_dict[nutrient.data_name] = nutrient

fats = ['fat', 'mono-unsaturated', 'poly-unsaturated', 'saturated', 'trans', 'cholesterol']

proteins = ['protein', 'histidine', 'isoleucine', 'leucine', 'lysine', 'methionine', 'phenylalanine', 'threonine',
            'tryptophan', 'valine', 'arginine', 'cystine', 'glycine', 'proline', 'tyrosine', 'alanine',
            'aspartic-acid', 'glutamic-acid', 'serine', 'hydroxyproline']

carbohydrates = ['carbohydrate', 'fiber', 'sugar', 'starch', 'sucrose', 'glucose', 'fructose', 'lactose', 'maltose',
                 'galactose']

minerals = ['calcium', 'copper', 'iron', 'magnesium', 'manganese', 'molybdenum', 'phosphorus', 'potassium',
            'selenium', 'sodium', 'zinc']

vitamins = ['vitamin-a', 'retinol', 'thiamin', 'riboflavin', 'niacin', 'pantothenic-acid', 'vitamin-b6', 'biotin',
            'folate', 'folic-acid', 'vitamin-b12', 'choline', 'vitamin-c', 'vitamin-d', 'vitamin-e', 'phylloquinone',
            'menaquinone']

alkaloids = ['caffeine', 'theobromine']


class EnergyDistribution:
    """Defines an energy distribution in fats, proteins and carbs."""
    def __init__(self, protein_amount, carb_amount, fat_amount):
        self.protein_factor = 4
        self.carbohydrate_factor = 4
        self.fat_factor = 8
        self.energy_protein = protein_amount * self.protein_factor
        self.energy_carb = carb_amount * self.carbohydrate_factor
        self.energy_fat = fat_amount * self.fat_factor
        self.energy_total = self.energy_protein + self.energy_carb + self.energy_fat
        self.protein_ratio = self.energy_protein / self.energy_total
        self.carbohydrate_ratio = self.energy_carb / self.energy_total
        self.fat_ratio = self.energy_fat / self.energy_total
