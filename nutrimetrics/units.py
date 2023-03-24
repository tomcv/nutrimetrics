# SPDX-FileCopyrightText: 2023-present Thomas Civeit <thomas@civeit.com>
#
# SPDX-License-Identifier: MIT
"""Defines units and unit converters.

Energy is always internally stored in kcal.
Nutrient amount is always internally stored in gram.
"""


class Unit:
    """Defines a unit."""
    def __init__(self, name, symbol, internal_factor):
        self.name = name
        self.symbol = symbol
        self.internal_factor = internal_factor


unit_kcal = Unit('kilocalorie', 'kcal', internal_factor=1.0)
unit_gram = Unit('gram', 'g', internal_factor=1.0)
unit_milligram = Unit('milligram', 'mg', internal_factor=1e3)
unit_microgram = Unit('microgram', 'µg', internal_factor=1e6)


def convert_amount(amount, unit):
    """Convert amount from specified unit to internal value."""
    if unit in ['kcal', 'g']:
        return amount
    elif unit == 'mg':
        return 1e-3 * amount
    elif unit == 'µg':
        return 1e-6 * amount
    else:
        print(f"ERROR: unit '{unit}' is unknown")
        return 0
