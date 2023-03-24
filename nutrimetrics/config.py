# SPDX-FileCopyrightText: 2023-present Thomas Civeit <thomas@civeit.com>
#
# SPDX-License-Identifier: MIT
"""User's configuration."""

from pathlib import Path
import os
import json
import importlib.resources as rsc
import shutil


config_dir = Path(Path.home(), '.nutrimetrics')
config_file = Path(config_dir, 'config.json')
foods_dir = Path(config_dir, 'foods')
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
    # ~/.nutrimetrics/samples/
    if not samples_dir.exists():
        shutil.copytree(rsc.files('nutrimetrics.resources').joinpath('samples'), samples_dir)


def read_config():
    """Read user's configuration and return configuration dictionary."""
    initialize()
    with open(config_file, 'r') as file:
        config = json.load(file)
    return config
