# SPDX-FileCopyrightText: 2023-present Thomas Civeit <thomas@civeit.com>
#
# SPDX-License-Identifier: MIT
"""User's configuration."""

from pathlib import Path
import os
from jsmin import jsmin
import json
from json.decoder import JSONDecodeError
import importlib.resources as rsc
import shutil


config_dir = Path(Path.home(), '.nutrimetrics')
config_file = Path(config_dir, 'config.json')
foods_dir = Path(config_dir, 'foods')
dri_dir = Path(config_dir, 'dri')
samples_dir = Path(config_dir, 'samples')


def initialize():
    """Create directory structure and default files."""
    # ~/.nutrimetrics/
    if not config_dir.exists():
        os.mkdir(config_dir)
    # ~/.nutrimetrics/config.json
    if not config_file.exists():
        shutil.copy(rsc.files('nutrimetrics.resources').joinpath('config.json'), config_file)
    # ~/.nutrimetrics/foods/
    if not foods_dir.exists():
        shutil.copytree(rsc.files('nutrimetrics.resources').joinpath('foods'), foods_dir)
    # ~/.nutrimetrics/dri/
    if not dri_dir.exists():
        shutil.copytree(rsc.files('nutrimetrics.resources').joinpath('dri'), dri_dir)
    # ~/.nutrimetrics/samples/
    if not samples_dir.exists():
        shutil.copytree(rsc.files('nutrimetrics.resources').joinpath('samples'), samples_dir)


def read_json(json_file):
    """Read JSON file that may have comments"""
    with open(json_file, 'r') as file:
        try:
            data = json.loads(jsmin(file.read()))
        except JSONDecodeError as e:
            print(f"ERROR: JSON file '{json_file.absolute()}' badly formatted")
            print(f"{e.msg}:")
            begin = max(0, e.pos - 50)
            end = min(len(e.doc), e.pos + 50)
            print(f"...\n{e.doc[begin:end]}\n...")
            data = None
    return data


def read_config():
    """Read user's configuration and return configuration dictionary."""
    initialize()
    return read_json(config_file)


def get_config_file_tree():
    tree = f'{config_dir.absolute()}\n'
    tree += f'├── config.json\n'
    tree += f'├── foods\n'
    n_food = 0
    for file in [Path(dri_dir, f) for f in sorted(os.listdir(foods_dir))]:
        if file.suffix == '.json':
            n_food += 1
    tree += f'│   └── {n_food} nutrient profiles defined\n'
    tree += f'├── dri\n'
    dri_files = [Path(dri_dir, f) for f in sorted(os.listdir(dri_dir))]
    for file in dri_files:
        if file.suffix == '.json':
            tree += '│   ' + ('└' if file == dri_files[-1] else '├') + f'── {file.name}\n'
    tree += f'└── samples\n'
    samples_files = [Path(dri_dir, f) for f in sorted(os.listdir(samples_dir))]
    for file in samples_files:
        if file.suffix == '.json':
            tree += '    ' + ('└' if file == samples_files[-1] else '├') + f'── {file.name}\n'
    return tree
