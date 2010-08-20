# -*- coding: utf-8 -*-

"""Helpers for Trage."""


import os
import gtk

from trage.trageconfig import get_data_file

import gettext
from gettext import gettext as _
gettext.textdomain('trage')

def get_builder(builder_file_name):
    """Return a fully-instantiated gtk.Builder instance from specified ui
    file

    :param builder_file_name: The name of the builder file, without extension.
        Assumed to be in the 'ui' directory under the data path.
    """
    # Look for the ui file that describes the user interface.
    ui_filename = get_data_file('ui', '%s.ui' % (builder_file_name,))
    if not os.path.exists(ui_filename):
        ui_filename = None

    builder = gtk.Builder()
    builder.set_translation_domain('trage')
    builder.add_from_file(ui_filename)
    return builder
