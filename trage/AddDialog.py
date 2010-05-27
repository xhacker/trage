# -*- coding: utf-8 -*-

import gtk
import gobject
import os
import shutil

import gettext
from gettext import gettext as _
gettext.textdomain('trage')

from trage.helpers import get_builder

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

    def update_stores(self, widget = None):
        self.file_store.clear()
        filechooser = self.builder.get_object('filechooser_probbasedir')
        basedir = filechooser.get_filename()
        files = os.listdir(basedir)
        for f in files:
            if os.path.isfile(os.path.join(basedir, f)):
                self.file_store.append([f])

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
        self.file_store = gtk.ListStore(gobject.TYPE_STRING)
        cell_render.set_property('editable', True)
        cell_render.set_property('model', self.file_store)
        cell_render.set_property("text-column", 0)
        cell_render.set_property("has-entry", False)

        cell_render.connect("edited", self.cell_edited, COLUMN_INFILE)

        column = gtk.TreeViewColumn(_('Input File'), cell_render, text = COLUMN_INFILE)
        treeview.append_column(column)

        # Column Ans
        cell_render = gtk.CellRendererCombo()
        cell_render.set_property('editable', True)
        cell_render.set_property('model', self.file_store)
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

        self.update_stores()

    def tp_more(self, widget):
        '''增加一个测试点'''
        if self.tp == 1:
            # 使减少测试点按钮恢复可用
            button_less = self.builder.get_object('button_tpless')
            button_less.set_sensitive(True)
        self.tp += 1

        # Add row
        self.model.append([self.tp, '', '', 0.5, 100])

    def tp_less(self, widget):
        '''减少一个测试点'''
        if self.tp == 1:
            return

        # Delete row
        model_iter = self.model.get_iter_first()
        while self.model.iter_next(model_iter) is not None:
            model_iter = self.model.iter_next(model_iter)
        self.model.remove(model_iter)

        self.tp -= 1

        if self.tp == 1:
            # 使减少测试点按钮不可用
            button_less = self.builder.get_object('button_tpless')
            button_less.set_sensitive(False)

    def add(self, widget):
        # Check
        entry_probtitle = self.builder.get_object('entry_probtitle')
        entry_probname = self.builder.get_object('entry_probname')

        # Get a new problem ID
        prob_dir = os.path.join(os.getenv("HOME"), ".trage/problem/user")
        for i in range(999999):
            if not os.path.exists(os.path.join(prob_dir, str(i))):
                break
        prob_dir = os.path.join(prob_dir, str(i))

        # Make problem dir
        os.mkdir(prob_dir)
        filechooser = self.builder.get_object('filechooser_probbasedir')
        basedir = filechooser.get_filename()
        model_iter = self.model.get_iter_first()
        for i in range(self.tp):
            # Copy input file
            src = self.model.get_value(model_iter, COLUMN_INFILE)
            src = os.path.join(basedir, src)
            dst = os.path.join(prob_dir, str(i) + '.in')
            shutil.copy(src, dst)

            # Copy answer file
            src = self.model.get_value(model_iter, COLUMN_ANSFILE)
            src = os.path.join(basedir, src)
            dst = os.path.join(prob_dir, str(i) + '.ans')
            shutil.copy(src, dst)

            model_iter = self.model.iter_next(model_iter)

        # Write problem config file
        import ConfigParser
        config = ConfigParser.RawConfigParser()

        config.add_section('main')
        config.set('main', 'name', entry_probname.get_text())
        config.set('main', 'title', entry_probtitle.get_text())
        config.add_section('test_point')
        config.set('test_point', 'test_point_count', self.tp)
        # TODO
        #config.set('test_point', 'time_limit_0', 'fun')
        #config.set('test_point', 'mem_limit_0', 'Python')

        with open(os.path.join(prob_dir, 'problem.conf'), 'wb') as configfile:
            config.write(configfile)

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
