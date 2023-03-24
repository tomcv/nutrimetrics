# SPDX-FileCopyrightText: 2023-present Thomas Civeit <thomas@civeit.com>
#
# SPDX-License-Identifier: MIT
"""Workbook interface to generate Excel reports."""

import xlsxwriter
from nutrimetrics.nutrients import nutrients_list, proteins, carbohydrates, fats, minerals, vitamins, alkaloids


class WorkbookGenerator:
    """Workbook interface to generate Excel reports."""
    def __init__(self, settings, dri_dict):
        self.settings = settings
        self.dri_dict = dri_dict
        self.workbook = None

    def generate(self, out_file, meal_plan, foods_dict):
        self.workbook = xlsxwriter.Workbook(out_file)
        self.create_meals_worksheet(meal_plan)
        self.create_foods_worksheet(foods_dict)
        self.workbook.close()
        print(f'Workbook created in {out_file.absolute()}')

    def create_meals_worksheet(self, meal_plan):
        worksheet = self.workbook.add_worksheet(f'Meals - {meal_plan.name}')
        self.write_headers(worksheet)
        row_i = 0
        for meal in meal_plan.meals:
            row_i += 1
            column_i = 0
            fmt = self.get_format(
                font_color=self.settings['colors']['food'][1],  # inverse fg/bg colors
                bg_color=self.settings['colors']['food'][0],
                bold=True,
                align='left')
            worksheet.write(row_i, column_i, meal.name, fmt)
            row_i, column_i = self.write_values(worksheet, row_i, foods=meal.foods)
            row_i, column_i = self.write_values(worksheet, row_i, foods=[meal.total],
                                                force_bold=True, force_bg_color=self.settings['total_bg_color'])
        row_i += 1
        row_i, column_i = self.write_values(worksheet, row_i, foods=[meal_plan.total],
                                            force_bold=True, force_bg_color=self.settings['grand_total_bg_color'])
        row_i, column_i = self.write_energy(worksheet, row_i, meal_plan)
        row_i, column_i = self.write_dri(worksheet, row_i, meal_plan)
        self.write_columns_separators(worksheet, row_i)
        self.set_columns_width(worksheet, column_i)
        worksheet.freeze_panes('B2')

    def create_foods_worksheet(self, foods_dict):
        worksheet = self.workbook.add_worksheet('Foods')
        self.write_headers(worksheet)
        row_i, column_i = self.write_values(worksheet, row_i=0, foods=foods_dict.values())
        self.write_columns_separators(worksheet, row_i)
        self.set_columns_width(worksheet, column_i)
        worksheet.freeze_panes('B2')

    def get_format(self, font_color, bg_color, bold, align, border=None, rotation=None):
        fmt = {
            'font_name': self.settings['font_name'],
            'font_size': self.settings['font_size'],
            'font_color': font_color,
            'bold': bold,
            'align': align,
            'valign': 'bottom',  # force bottom vertical alignment
            'num_format': self.settings['number_format'],
        }
        if bg_color:
            fmt['bg_color'] = bg_color
        if border:
            fmt['border'] = border
        if rotation:
            fmt['rotation'] = rotation
        return self.workbook.add_format(fmt)

    def get_colors(self, nutrient_data_name):
        if nutrient_data_name == 'energy':
            return self.settings['colors']['energy']
        elif nutrient_data_name == 'water':
            return self.settings['colors']['water']
        elif nutrient_data_name in proteins:
            return self.settings['colors']['proteins']
        elif nutrient_data_name in carbohydrates:
            return self.settings['colors']['carbohydrates']
        elif nutrient_data_name in fats:
            return self.settings['colors']['fats']
        elif nutrient_data_name in minerals:
            return self.settings['colors']['minerals']
        elif nutrient_data_name in vitamins:
            return self.settings['colors']['vitamins']
        elif nutrient_data_name in alkaloids:
            return self.settings['colors']['alkaloids']

    @staticmethod
    def get_header_label(nutrient):
        return f'{nutrient.display_name} [{nutrient.display_unit.symbol}]'

    @staticmethod
    def convert(nutrient, amount):
        return nutrient.display_unit.internal_factor * amount

    def write_headers(self, worksheet):
        row_i, column_i = 0, 0
        fmt = self.get_format(
            font_color=self.settings['colors']['food'][0],
            bg_color=self.settings['colors']['food'][1],
            bold=True,
            align='left')
        worksheet.write(row_i, column_i, 'Food', fmt)
        column_i += 1
        fmt = self.get_format(
            font_color=self.settings['colors']['amount'][0],
            bg_color=self.settings['colors']['amount'][1],
            bold=True,
            align='left',
            border=1,
            rotation=45)
        worksheet.write(row_i, column_i, 'Amount [g]', fmt)
        for nutrient in nutrients_list:
            if nutrient.data_name in self.settings['do_not_display']:
                continue
            column_i += 1
            font_color, bg_color = self.get_colors(nutrient.data_name)
            fmt = self.get_format(
                font_color=font_color,
                bg_color=bg_color,
                bold=True,
                align='left',
                border=1,
                rotation=45)
            worksheet.write(row_i, column_i, self.get_header_label(nutrient), fmt)

    def write_values(self, worksheet, row_i, foods, force_bold=False, force_bg_color=None):
        for food in foods:
            row_i += 1
            column_i = 0
            fmt = self.get_format(
                font_color=self.settings['colors']['food'][0],
                bg_color=(force_bg_color if force_bg_color else None),
                bold=force_bold,
                align='left')
            worksheet.write(row_i, column_i, food.name, fmt)
            column_i += 1
            fmt = self.get_format(
                font_color=self.settings['colors']['amount'][0],
                bg_color=(force_bg_color if force_bg_color else None),
                bold=False,
                align='right')
            worksheet.write(row_i, column_i, food.amount, fmt)
            for nutrient in nutrients_list:
                if nutrient.data_name in self.settings['do_not_display']:
                    continue
                column_i += 1
                font_color, bg_color = self.get_colors(nutrient.data_name)
                fmt = self.get_format(
                    font_color=font_color,
                    bg_color=(force_bg_color if force_bg_color else None),
                    bold=False,
                    align='right')
                value = self.convert(nutrient, food.nutrients[nutrient.data_name])
                worksheet.write(row_i, column_i, value, fmt)
        return row_i, column_i

    def write_energy(self, worksheet, row_i, meal_plan):
        column_i = 0
        row_i += 1
        fmt = self.get_format(
            font_color=self.settings['colors']['food'][0],
            bg_color=None,
            bold=True,
            align='left')
        worksheet.write(row_i, column_i, 'Energy [%]', fmt)
        column_i = 1
        for nutrient in nutrients_list:
            if nutrient.data_name in self.settings['do_not_display']:
                continue
            column_i += 1
            font_color, bg_color = self.get_colors(nutrient.data_name)
            fmt = self.get_format(
                font_color=font_color,
                bg_color=self.settings['energy_bg_color'],
                bold=False,
                align='right')
            if nutrient.data_name == 'protein':
                worksheet.write(row_i, column_i, 100 * meal_plan.distribution.protein_ratio, fmt)
            elif nutrient.data_name == 'carbohydrate':
                worksheet.write(row_i, column_i, 100 * meal_plan.distribution.carbohydrate_ratio, fmt)
            elif nutrient.data_name == 'fat':
                worksheet.write(row_i, column_i, 100 * meal_plan.distribution.fat_ratio, fmt)
        return row_i, column_i

    def write_dri(self, worksheet, row_i, meal_plan):
        # write DRI values
        row_i += 1
        column_i = 0
        fmt = self.get_format(
            font_color=self.settings['colors']['food'][0],
            bg_color=None,
            bold=True,
            align='left')
        worksheet.write(row_i, column_i, 'Dietary Reference Intakes', fmt)
        column_i = 1
        for nutrient in nutrients_list:
            if nutrient.data_name in self.settings['do_not_display']:
                continue
            column_i += 1
            if nutrient.data_name in self.dri_dict:
                font_color, bg_color = self.get_colors(nutrient.data_name)
                fmt = self.get_format(
                    font_color=font_color,
                    bg_color=None,
                    bold=False,
                    align='right')
                worksheet.write(row_i, column_i, self.convert(nutrient, self.dri_dict[nutrient.data_name]), fmt)
        # write DRI percentage
        row_i += 1
        column_i = 0
        fmt = self.get_format(
            font_color=self.settings['colors']['food'][0],
            bg_color=None,
            bold=True,
            align='left')
        worksheet.write(row_i, column_i, 'DRI [%]', fmt)
        column_i = 1
        for nutrient in nutrients_list:
            if nutrient.data_name in self.settings['do_not_display']:
                continue
            column_i += 1
            if nutrient.data_name in self.dri_dict:
                font_color, bg_color = self.get_colors(nutrient.data_name)
                percent = 100 * meal_plan.dri_ratio[nutrient.data_name]
                bg_color = (self.settings['dri_negative_bg_color'] if percent < 100
                            else self.settings['dri_positive_bg_color'])
                fmt = self.get_format(
                    font_color=font_color,
                    bg_color=bg_color,
                    bold=False,
                    align='right')
                worksheet.write(row_i, column_i, percent, fmt)
        return row_i, column_i

    def write_columns_separators(self, worksheet, bottom_row):
        border_format = self.workbook.add_format({'left': 1})
        for column in self.settings['columns_separators']:
            worksheet.conditional_format(1, column, bottom_row, column,
                                         {'type': 'blanks', 'format': border_format})
            worksheet.conditional_format(1, column, bottom_row, column,
                                         {'type': 'no_blanks', 'format': border_format})

    def set_columns_width(self, worksheet, last_column):
        worksheet.set_column_pixels(0, 0, self.settings['column_pixels_food'])
        for i in range(last_column):
            worksheet.set_column_pixels(i+1, i+1, self.settings['column_pixels_nutrient'])
