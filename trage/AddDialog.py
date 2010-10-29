# -*- coding: utf-8 -*-

import gtk
import gobject
import os

import shutil
import string

import gettext
from gettext import gettext as _
gettext.textdomain('trage')

from trage.helpers import get_builder, get_textview_text
from trage.common.general import *

(
    COLUMN_ID,
    COLUMN_INFILE,
    COLUMN_ANSFILE,
    COLUMN_TIMELIMIT,
    COLUMN_MEMLIMIT,
) = range(5)

class AddDialog(gtk.Window):
    __gtype_name__ = "AddDialog"

    def __new__(cls):
        """Special static method that's automatically called by Python when
        constructing a new instance of this class.

        Returns a fully instantiated AddFooDialog object.
        """
        builder = get_builder('AddDialog')
        new_object = builder.get_object("add_dialog")
        new_object.finish_init(builder)
        return new_object

    def finish_init(self, builder):
        self.builder = builder
        self.builder.connect_signals(self)

        # Code for other initialization actions

        self.init_treeview()

        self.tp = 0
        self.tp_more(None)

        # 使减少测试点按钮不可用
        button_less = self.builder.get_object('button_tpless')
        button_less.set_sensitive(False)

    def get_last_iter(self, model):
        iter = model.get_iter_first()
        if iter:
            while model.iter_next(iter) is not None:
                iter = model.iter_next(iter)
        return iter

    def update_model_file(self, widget = None):
        self.model_file.clear()
        filechooser = self.builder.get_object('filechooser_probbasedir')
        base_dir = filechooser.get_filename()
        files = os.listdir(base_dir)
        files.sort()
        for f in files:
            if os.path.isfile(os.path.join(base_dir, f)):
                self.model_file.append([f])

    def cell_edited(self, cellrenderertext, path, new_val, column):
        iter = self.model.get_iter(path)
        if column in [COLUMN_TIMELIMIT, COLUMN_MEMLIMIT]:
            self.model.set_value(iter, column, float(new_val))
        else:
            self.model.set_value(iter, column, new_val)

    def init_treeview(self):
        treeview = self.builder.get_object('treeview_tp')

        # create model
        model = gtk.ListStore(
                            gobject.TYPE_INT,
                            gobject.TYPE_STRING,
                            gobject.TYPE_STRING,
                            gobject.TYPE_FLOAT,
                            gobject.TYPE_INT)

        treeview.set_model(model)

        column = gtk.TreeViewColumn('', gtk.CellRendererText(), text = COLUMN_ID)
        treeview.append_column(column)

        # Column Input
        cell_render = gtk.CellRendererCombo()
        self.model_file = gtk.ListStore(gobject.TYPE_STRING)
        cell_render.set_property('editable', True)
        cell_render.set_property('model', self.model_file)
        cell_render.set_property("text-column", 0)
        cell_render.set_property("has-entry", False)

        cell_render.connect("edited", self.cell_edited, COLUMN_INFILE)

        column = gtk.TreeViewColumn(_('Input File'), cell_render, text = COLUMN_INFILE)
        treeview.append_column(column)

        # Column Ans
        cell_render = gtk.CellRendererCombo()
        cell_render.set_property('editable', True)
        cell_render.set_property('model', self.model_file)
        cell_render.set_property("text-column", 0)
        cell_render.set_property("has-entry", False)

        cell_render.connect("edited", self.cell_edited, COLUMN_ANSFILE)

        column = gtk.TreeViewColumn(_('Answer File'), cell_render, text = COLUMN_ANSFILE)
        treeview.append_column(column)

        # Column Time
        cell_render = gtk.CellRendererText()
        cell_render.set_property('editable', True)

        cell_render.connect("edited", self.cell_edited, COLUMN_TIMELIMIT)

        column = gtk.TreeViewColumn(_('Time Limit'), cell_render, text = COLUMN_TIMELIMIT)
        treeview.append_column(column)

        # Column Mem
        cell_render = gtk.CellRendererText()
        cell_render.set_property('editable', True)

        cell_render.connect("edited", self.cell_edited, COLUMN_MEMLIMIT)

        column = gtk.TreeViewColumn(_('Mem Limit'), cell_render, text = COLUMN_MEMLIMIT)
        treeview.append_column(column)

        self.model = model
        self.treeview = treeview

        self.update_model_file()

    def tp_more(self, widget):
        '''增加一个测试点'''
        if self.tp == 1:
            # 使减少测试点按钮恢复可用
            button_less = self.builder.get_object('button_tpless')
            button_less.set_sensitive(True)
        self.tp += 1

        if self.tp == 1:
            time_limit = 1.0
            mem_limit = 32
        else:
            # Guess time limit and mem limit
            iter = self.get_last_iter(self.model)
            time_limit = self.model.get_value(iter, COLUMN_TIMELIMIT)
            mem_limit = self.model.get_value(iter, COLUMN_MEMLIMIT)

        # Guess input and output file
        input_filename = ''
        answer_filename = ''
        if self.tp == 1:
            pass
        else:
            if self.tp == 2:
                # Analysis first test point's file names
                self.input_pattern = ''
                iter = self.model.get_iter_first()
                input_filename_0 = self.model.get_value(iter, COLUMN_INFILE)

                if string.find(input_filename_0, '00') >= 0:
                    self.input_pattern = string.replace(input_filename_0, '00', '$NUM$', 1)
                    self.input_pattern_len = 2
                    self.input_pattern_start = 0
                elif string.find(input_filename_0, '01') >= 0:
                    self.input_pattern = string.replace(input_filename_0, '01', '$NUM$', 1)
                    self.input_pattern_len = 2
                    self.input_pattern_start = 1
                elif string.find(input_filename_0, '0') >= 0:
                    self.input_pattern = string.replace(input_filename_0, '0', '$NUM$', 1)
                    self.input_pattern_len = 1
                    self.input_pattern_start = 0
                elif string.find(input_filename_0, '1') >= 0:
                    self.input_pattern = string.replace(input_filename_0, '1', '$NUM$', 1)
                    self.input_pattern_len = 1
                    self.input_pattern_start = 1

                self.answer_pattern = ''
                iter = self.model.get_iter_first()
                answer_filename_0 = self.model.get_value(iter, COLUMN_ANSFILE)

                if string.find(answer_filename_0, '00') >= 0:
                    self.answer_pattern = string.replace(answer_filename_0, '00', '$NUM$', 1)
                    self.answer_pattern_len = 2
                    self.answer_pattern_start = 0
                elif string.find(answer_filename_0, '01') >= 0:
                    self.answer_pattern = string.replace(answer_filename_0, '01', '$NUM$', 1)
                    self.answer_pattern_len = 2
                    self.answer_pattern_start = 1
                elif string.find(answer_filename_0, '0') >= 0:
                    self.answer_pattern = string.replace(answer_filename_0, '0', '$NUM$', 1)
                    self.answer_pattern_len = 1
                    self.answer_pattern_start = 0
                elif string.find(answer_filename_0, '1') >= 0:
                    self.answer_pattern = string.replace(answer_filename_0, '1', '$NUM$', 1)
                    self.answer_pattern_len = 1
                    self.answer_pattern_start = 1

            if self.input_pattern:
                if self.input_pattern_len == 1:
                    num_str = str(self.tp + self.input_pattern_start - 1)
                elif self.input_pattern_len == 2:
                    num_str = '%02d' % (self.tp + self.input_pattern_start - 1)

                input_filename = string.replace(self.input_pattern, '$NUM$', num_str, 1)
                filechooser = self.builder.get_object('filechooser_probbasedir')
                base_dir = filechooser.get_filename()
                if not os.path.isfile(os.path.join(base_dir, input_filename)):
                    input_filename = ''
                    self.input_pattern = ''

            if self.answer_pattern:
                if self.answer_pattern_len == 1:
                    num_str = str(self.tp + self.answer_pattern_start - 1)
                elif self.answer_pattern_len == 2:
                    num_str = '%02d' % (self.tp + self.answer_pattern_start - 1)

                answer_filename = string.replace(self.answer_pattern, '$NUM$', num_str, 1)
                filechooser = self.builder.get_object('filechooser_probbasedir')
                base_dir = filechooser.get_filename()
                if not os.path.isfile(os.path.join(base_dir, answer_filename)):
                    answer_filename = ''
                    self.answer_pattern = ''

        # Add row
        self.model.append([self.tp, input_filename, answer_filename, time_limit, mem_limit])

    def tp_less(self, widget):
        '''减少一个测试点'''
        if self.tp == 1:
            return

        # Delete row
        iter = self.get_last_iter(self.model)
        self.model.remove(iter)

        self.tp -= 1

        if self.tp == 1:
            # 使减少测试点按钮不可用
            button_less = self.builder.get_object('button_tpless')
            button_less.set_sensitive(False)

    def alert(self, text):
        alert_dialog = gtk.MessageDialog(buttons = gtk.BUTTONS_OK, message_format = text)
        result = alert_dialog.run()
        alert_dialog.destroy()

    def add(self, widget):
        entry_probtitle = self.builder.get_object('entry_probtitle')
        entry_probname = self.builder.get_object('entry_probname')
        entry_difficulty = self.builder.get_object('entry_difficulty')
        textview_main = self.builder.get_object('textview_main')
        textview_input = self.builder.get_object('textview_input')
        textview_output = self.builder.get_object('textview_output')
        textview_hint = self.builder.get_object('textview_hint')
        textview_exampleinput = self.builder.get_object('textview_exampleinput')
        textview_exampleoutput = self.builder.get_object('textview_exampleoutput')
        prob_name = entry_probname.get_text()
        prob_title = entry_probtitle.get_text()
        difficulty = entry_difficulty.get_text()
        info_main = get_textview_text(textview_main)
        info_input = get_textview_text(textview_input)
        info_output = get_textview_text(textview_output)
        info_hint = get_textview_text(textview_hint)
        example_input = get_textview_text(textview_exampleinput)
        example_output = get_textview_text(textview_exampleoutput)
        filechooser = self.builder.get_object('filechooser_probbasedir')
        base_dir = filechooser.get_filename()

        # Check
        if not prob_title:
            self.alert(_('Please enter problem title.'))
            return

        if not prob_name:
            self.alert(_('Please enter problem name.'))
            return

        iter = self.model.get_iter_first()
        for i in range(self.tp):
            in_file = self.model.get_value(iter, COLUMN_INFILE)
            ans_file = self.model.get_value(iter, COLUMN_ANSFILE)

            if (not in_file) or (not ans_file):
                self.alert(_('Every test point should have a input file and a answer file.'))
                return

            in_file = os.path.join(base_dir, in_file)
            if not os.path.isfile(in_file):
                self.alert(_("Test point %d's input file not exist. Please select a valid file.") % (i + 1))
                self.update_model_file()
                return

            ans_file = os.path.join(base_dir, ans_file)
            if not os.path.isfile(ans_file):
                self.alert(_("Test point %d's answer file not exist. Please select a valid file.") % (i + 1))
                self.update_model_file()
                return

            iter = self.model.iter_next(iter)

        # Adding
        import sqlite3
        conn = sqlite3.connect(db_location)
        conn.text_factory = str
        c = conn.cursor()
        c.execute('''
        INSERT INTO problem
        (name, title, info_main, info_hint, info_input, info_output, example_input, example_output, difficulty) VALUES
        (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (prob_name, prob_title, info_main, info_hint, info_input, info_output, example_input, example_output, difficulty))
        prob_id = str(c.lastrowid)
        conn.commit()
        c.close()
        prob_dir = os.path.join(prob_root_dir, prob_id)
        os.mkdir(prob_dir)
        
        iter = self.model.get_iter_first()
        for i in range(self.tp):
            # Copy input file
            src = self.model.get_value(iter, COLUMN_INFILE)
            src = os.path.join(base_dir, src)
            dst = os.path.join(prob_dir, str(i) + '.in')
            shutil.copy(src, dst)

            # Copy answer file
            src = self.model.get_value(iter, COLUMN_ANSFILE)
            src = os.path.join(base_dir, src)
            dst = os.path.join(prob_dir, str(i) + '.ans')
            shutil.copy(src, dst)

            iter = self.model.iter_next(iter)

        # Write problem config file
        import ConfigParser
        config = ConfigParser.RawConfigParser()

        config.add_section('main')
        config.set('main', 'name', prob_name)
        config.set('main', 'title', prob_title)
        config.add_section('test_point')
        config.set('test_point', 'test_point_count', self.tp)

        iter = self.model.get_iter_first()
        for i in range(self.tp):
            time_limit = self.model.get_value(iter, COLUMN_TIMELIMIT)
            mem_limit = self.model.get_value(iter, COLUMN_MEMLIMIT)
            config.set('test_point', 'time_limit_' + str(i), time_limit)
            config.set('test_point', 'mem_limit_' + str(i), mem_limit)
            iter = self.model.iter_next(iter)

        with open(os.path.join(prob_dir, 'problem.conf'), 'wb') as config_file:
            config.write(config_file)

        self.destroy()

    def quit(self, widget):
        """quit - signal handler for closing the AddDialog"""
        self.destroy()

    def on_destroy(self, widget):
        """on_destroy - called when the AddDialog is close"""
        gtk.main_quit()

if __name__ == "__main__":
    dialog = AddDialog()
    dialog.show()
    gtk.main()
