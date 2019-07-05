#!/usr/bin/env python3
# # -*- coding: utf-8 -*-

"""
Manages configuration.
________________________________________________________________________________

Created by brightSPARK Labs
www.brightsparklabs.com
"""

# standard library
import io
import logging
import sys
from functools import reduce
from pathlib import Path

# vendor libraries
import coloredlogs
from ruamel.yaml import YAML

# ------------------------------------------------------------------------------
# LOGGING
# ------------------------------------------------------------------------------

FORMAT = '%(asctime)s %(levelname)s: %(message)s'
logger = logging.getLogger(__name__)
coloredlogs.install(logger=logger, fmt=FORMAT)

# ------------------------------------------------------------------------------
# INTERNAL CLASSES
# ------------------------------------------------------------------------------

class ConfigurationManager:
    """Manages the configuration"""

    def __init__(self, configuration_file):
        """Creates a manager for the specified file

        Args:
            configuration_file (str): Path to the configuration file to manage
        """
        self.configuration_file = Path(configuration_file)
        data = self.configuration_file.read_text(encoding='utf-8')
        self.yaml = YAML()
        self.configuration = self.yaml.load(data)

    def get(self, path):
        """Gets a value from the configuration.

        Args:
            path (str): Dot notation for the setting. E.g. insilico.external.database.host
        """
        try:
            return reduce(lambda e, k: e[k], path.split('.'), self.configuration)
        except:
            return ''

    def get_as_dict(self):
        return self.configuration

    def set(self, path, value):
        """Sets a value in the configuration.

        Args:
            path (str): Dot notation for the setting. E.g. insilico.external.database.host
            value: value for the setting
        """
        path_elements = path.split('.')
        parent_path = path_elements[:-1]

        # ensure parent path exists
        def ensure_path(parent, child):
            if not child in parent:
                parent[child] = {}
            return parent[child]
        reduce(ensure_path, parent_path, self.configuration)

        # set the value
        parent_element = reduce(lambda e, k: e[k], parent_path, self.configuration)
        parent_element[path_elements[-1]] = value

    def save(self):
        """Saves the configuration"""
        full_path = self.configuration_file.absolute().as_posix()
        logger.info(f'Saving configuration to [{full_path}] ...')
        with open(full_path, 'w') as config_file:
            self.yaml.dump(self.configuration, config_file)

    def dump(self, stream=sys.stdout):
        """Dumps the configuration to stdout"""
        self.yaml.dump(self.configuration, sys.stdout)