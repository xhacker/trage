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

def get_textview_text(textview):
    buffer = textview.get_buffer()
    start_iter = buffer.get_start_iter()
    end_iter = buffer.get_end_iter()
    return buffer.get_text(start_iter, end_iter)

def get_difficulty_text(difficulty):
    if difficulty is not 0 and not difficulty:
        difficulty = 2
    difficulty = int(difficulty)
    if difficulty < 0:
        difficulty = 0
    if difficulty > 5:
        difficulty = 5
    text = [
        '纯水',
        '略水',
        '还行',
        '微难',
        '暴难',
        '别碰'
    ]
    return text[difficulty]

def nl2br(text):
    if text is None:
        return ''
    return text.replace("\n","<br />\n")

def format(text, prob_id):
    for i in range(100):
        img_holder = "{{{IMG%d}}}" % i
        if img_holder in text:
            text = text.replace(img_holder, '<img src="/problem/%s/img/%d" />' % (prob_id, i))
    return nl2br(text)
