# SPDX-FileCopyrightText: 2023-present Thomas Civeit <thomas@civeit.com>
#
# SPDX-License-Identifier: MIT
"""Workbook interface to generate Excel reports."""

import xlsxwriter
from nutrimetrics.nutrients import nutrients_list, proteins, carbohydrates, fats, minerals, vitamins, alkaloids


class WorkbookGenerator:
    """Workbook interface to generate Excel reports."""
    def __init__(self, settings):
        self.settings = settings
        self.workbook = None

    def generate(self, out_file, meal_plan, foods_dict):
        self.workbook = xlsxwriter.Workbook(out_file)
        self.create_meals_worksheet(meal_plan)
        self.create_target_worksheet(meal_plan)
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
        row_i, column_i = self.write_target_and_dri(worksheet, row_i, meal_plan)
        self.write_columns_separators(worksheet, row_i)
        self.set_columns_width(worksheet, column_i)
        worksheet.freeze_panes('B2')

    def create_target_worksheet(self, meal_plan):
        worksheet = self.workbook.add_worksheet('Target')
        fmt_label = self.get_format(
            font_color=self.settings['target']['font_color'],
            bg_color=None,
            bold=False,
            align='left',
            border=1)
        fmt_value = self.get_format(
            font_color=self.settings['target']['font_color'],
            bg_color=None,
            bold=False,
            align='right',
            border=1)
        fmt_body_mass_label = self.get_format(
            font_color=self.settings['target']['font_color'],
            bg_color=self.settings['target']['body_mass_bg_color'],
            bold=False,
            align='left',
            border=1)
        fmt_body_mass_value = self.get_format(
            font_color=self.settings['target']['font_color'],
            bg_color=self.settings['target']['body_mass_bg_color'],
            bold=False,
            align='right',
            border=1)
        fmt_body_fat_label = self.get_format(
            font_color=self.settings['target']['font_color'],
            bg_color=self.settings['target']['body_fat_bg_color'],
            bold=False,
            align='left',
            border=1)
        fmt_body_fat_value = self.get_format(
            font_color=self.settings['target']['font_color'],
            bg_color=self.settings['target']['body_fat_bg_color'],
            bold=False,
            align='right',
            border=1)
        fmt_lean_body_mass_label = self.get_format(
            font_color=self.settings['target']['font_color'],
            bg_color=self.settings['target']['lean_body_mass_bg_color'],
            bold=False,
            align='left',
            border=1)
        fmt_lean_body_mass_value = self.get_format(
            font_color=self.settings['target']['font_color'],
            bg_color=self.settings['target']['lean_body_mass_bg_color'],
            bold=False,
            align='right',
            border=1)
        fmt_energy_label = self.get_format(
            font_color=self.settings['colors']['energy'][0],
            bg_color=self.settings['colors']['energy'][1],
            bold=False,
            align='left',
            border=1)
        fmt_energy_value = self.get_format(
            font_color=self.settings['colors']['energy'][0],
            bg_color=self.settings['colors']['energy'][1],
            bold=False,
            align='right',
            border=1)
        fmt_annotate = self.get_format(
            font_color=self.settings['target']['font_color'],
            bg_color=None,
            bold=False,
            align='left',
            italic=True)
        # parameters
        worksheet.write(0, 0, 'Body Mass (g)', fmt_body_mass_label)
        worksheet.write(0, 1, meal_plan.target.body_mass, fmt_body_mass_value)
        worksheet.write(1, 0, 'Body Fat (%)', fmt_body_fat_label)
        worksheet.write(1, 1, meal_plan.target.body_fat_ratio * 100, fmt_body_fat_value)
        worksheet.write(2, 0, 'Activity Factor', fmt_label)
        worksheet.write(2, 1, meal_plan.target.activity_factor, fmt_value)
        worksheet.write(3, 0, 'Minimum Protein Factor', fmt_label)
        worksheet.write(3, 1, meal_plan.target.minimum_protein_factor, fmt_value)
        worksheet.write(4, 0, 'Minimum Fat Factor', fmt_label)
        worksheet.write(4, 1, meal_plan.target.minimum_fat_factor, fmt_value)
        # calculated values
        worksheet.write(6, 0, 'Lean Body Mass (g)', fmt_lean_body_mass_label)
        worksheet.write(6, 1, meal_plan.target.lean_body_mass, fmt_lean_body_mass_value)
        worksheet.write(7, 0, 'Resting Daily Energy Expenditure (kcal)', fmt_label)
        worksheet.write(7, 1, meal_plan.target.resting_energy, fmt_value)
        worksheet.write(8, 0, 'Basal Metabolic Rate (kcal)', fmt_energy_label)
        worksheet.write(8, 1, meal_plan.target.basal_metabolic_rate, fmt_energy_value)
        worksheet.write(9, 0, 'Minimum Protein (g)', fmt_label)
        worksheet.write(9, 1, meal_plan.target.minimum_protein, fmt_value)
        worksheet.write(10, 0, 'Minimum Fat (g)', fmt_label)
        worksheet.write(10, 1, meal_plan.target.minimum_fat, fmt_value)
        # add annotations
        worksheet.write(0, 3, "Meal plan parameters", fmt_annotate)
        worksheet.write(7, 3, "Katch–McArdle formula", fmt_annotate)
        worksheet.write(8, 3, "BMR based on activity factor", fmt_annotate)
        # set columns width
        worksheet.set_column_pixels(0, 0, self.settings['target']['column_pixels_label'])
        worksheet.set_column_pixels(1, 1, self.settings['target']['column_pixels_value'])
        worksheet.set_column_pixels(2, 2, self.settings['target']['column_pixels_separator'])

    def create_foods_worksheet(self, foods_dict):
        worksheet = self.workbook.add_worksheet('Foods')
        self.write_headers(worksheet)
        row_i, column_i = self.write_values(worksheet, row_i=0, foods=foods_dict.values(), comment=True)
        self.write_columns_separators(worksheet, row_i)
        self.set_columns_width(worksheet, column_i)
        worksheet.freeze_panes('B2')

    def get_format(self, font_color, bg_color, bold, align, border=None, rotation=None, italic=None):
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
        if italic:
            fmt['italic'] = italic
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

    def write_values(self, worksheet, row_i, foods, comment=False, force_bold=False, force_bg_color=None):
        comments_options = {
            'font_name': self.settings['font_name'],
            'font_size': self.settings['font_size'],
            'width': 250,
        }
        for food in foods:
            row_i += 1
            column_i = 0
            fmt = self.get_format(
                font_color=self.settings['colors']['food'][0],
                bg_color=(force_bg_color if force_bg_color else None),
                bold=force_bold,
                align='left')
            worksheet.write(row_i, column_i, food.name, fmt)
            if comment:
                worksheet.write_comment(row_i, column_i, food.description, comments_options)
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
            bold=False,
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

    def write_target_and_dri(self, worksheet, row_i, meal_plan):
        # write DRI values
        row_i += 1
        column_i = 0
        fmt = self.get_format(
            font_color=self.settings['colors']['food'][0],
            bg_color=None,
            bold=False,
            align='left')
        worksheet.write(row_i, column_i, f'Target & DRI ({meal_plan.dri_name})', fmt)
        column_i = 1
        for nutrient in nutrients_list:
            if nutrient.data_name in self.settings['do_not_display']:
                continue
            column_i += 1
            if nutrient.data_name in meal_plan.dri_dict:
                font_color, bg_color = self.get_colors(nutrient.data_name)
                fmt = self.get_format(
                    font_color=font_color,
                    bg_color=None,
                    bold=False,
                    align='right')
                worksheet.write(row_i, column_i,
                                self.convert(nutrient, meal_plan.dri_dict[nutrient.data_name]), fmt)
        # write DRI percentage
        row_i += 1
        column_i = 0
        fmt = self.get_format(
            font_color=self.settings['colors']['food'][0],
            bg_color=None,
            bold=False,
            align='left')
        worksheet.write(row_i, column_i, 'Target & DRI [%]', fmt)
        column_i = 1
        for nutrient in nutrients_list:
            if nutrient.data_name in self.settings['do_not_display']:
                continue
            column_i += 1
            if nutrient.data_name in meal_plan.dri_dict:
                font_color, bg_color = self.get_colors(nutrient.data_name)
                percent = 100 * meal_plan.dri_ratio[nutrient.data_name]
                if percent >= 300:
                    bg_color = self.settings['dri_colors']['excess_3']
                elif percent >= 200:
                    bg_color = self.settings['dri_colors']['excess_2']
                elif percent >= 100:
                    bg_color = self.settings['dri_colors']['excess_1']
                elif percent >= 80:
                    bg_color = self.settings['dri_colors']['deficit_1']
                elif percent >= 60:
                    bg_color = self.settings['dri_colors']['deficit_2']
                else:
                    bg_color = self.settings['dri_colors']['deficit_3']
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
            for cell_type in ['blanks', 'no_blanks']:
                worksheet.conditional_format(1, column, bottom_row, column,
                                             {'type': cell_type, 'format': border_format})

    def set_columns_width(self, worksheet, last_column):
        worksheet.set_column_pixels(0, 0, self.settings['column_pixels_food'])
        for i in range(last_column):
            worksheet.set_column_pixels(i+1, i+1, self.settings['column_pixels_nutrient'])
