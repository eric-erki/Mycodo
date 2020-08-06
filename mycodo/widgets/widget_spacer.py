# coding=utf-8
#
#  widget_spacer.py - Spacer dashboard widget
#
#  Copyright (C) 2017  Kyle T. Gabriel
#
#  This file is part of Mycodo
#
#  Mycodo is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Mycodo is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Mycodo. If not, see <http://www.gnu.org/licenses/>.
#
#  Contact at kylegabriel.com
#
import importlib.util
import logging
import os
import textwrap
import threading
import time

from flask import flash
from flask_babel import lazy_gettext

from mycodo.config import PATH_PYTHON_CODE_USER
from mycodo.widgets.base_widget import AbstractWidget
from mycodo.databases.models import Widget
from mycodo.utils.code_verification import create_python_file
from mycodo.utils.code_verification import test_python_code
from mycodo.utils.system_pi import parse_custom_option_values_json
from mycodo.utils.widgets import parse_widget_information

logger = logging.getLogger(__name__)

def constraints_pass_positive_value(mod_widget, value):
    """
    Check if the user widget is acceptable
    :param mod_widget: SQL object with user-saved Input options
    :param value: float or int
    :return: tuple: (bool, list of strings)
    """
    errors = []
    all_passed = True
    # Ensure value is positive
    if value <= 0:
        all_passed = False
        errors.append("Must be a positive value")
    return all_passed, errors, mod_widget


WIDGET_INFORMATION = {
    'widget_name_unique': 'WIDGET_SPACER',
    'widget_name': 'Spacer',
    'widget_library': '',
    'no_class': True,

    'message': 'This widget is a simple widget to use as a spacer, which includes the ability to set text in its contents.',

    'widget_width': 20,
    'widget_height': 2,

    'dependencies_module': [],

    'widget_dashboard_head': """<!-- No head content -->""",
    'widget_dashboard_body': """<span style="font-size: {{custom_options_values_widgets[each_widget.unique_id]['font_em_body']}}em">{{custom_options_values_widgets[each_widget.unique_id]['body_text']}}</span>""",
    'widget_dashboard_js': """<!-- No JS content -->""",
    'widget_dashboard_js_ready': """<!-- No JS ready content -->""",
    'widget_dashboard_js_ready_end': """<!-- No JS ready end content -->""",

    'custom_options': [
        {
            'id': 'font_em_body',
            'type': 'float',
            'default_value': 1.5,
            'constraints_pass': constraints_pass_positive_value,
            'name': 'Body Font Size (em)',
            'phrase': 'The font size of the body text'
        },
        {
            'id': 'body_text',
            'type': 'text',
            'default_value': "",
            'name': 'Body Text',
            'phrase': 'The body text of the widget'
        },
    ]
}
