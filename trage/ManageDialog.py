# -*- coding: utf-8 -*-

import gtk
import gobject
import os
import shutil

import gettext
from gettext import gettext as _
gettext.textdomain('trage')

from trage import (
    AddDialog)
from trage.common.problem import Problem
from trage.helpers import get_builder

(
    COLUMN_ID,
    COLUMN_NAME,
    COLUMN_TITLE,
) = range(3)

class ManageDialog(gtk.Window):
    __gtype_name__ = "ManageDialog"

    def __new__(cls):
        """Special static method that's automatically called by Python when
        constructing a new instance of this class.

        Returns a fully instantiated ManageFooDialog object.
        """
        builder = get_builder('ManageDialog')
        new_object = builder.get_object("manage_dialog")
        new_object.finish_init(builder)
        return new_object

    def finish_init(self, builder):
        self.builder = builder
        self.builder.connect_signals(self)

        self.init_treeview()
        self.button_delete = self.builder.get_object('button_delete')

        self.button_delete.set_sensitive(0)

    def update_model(self):
        # TODO: move duplicated codes to common/problem.py (get_prob_list)
        self.model.clear()
        prob_dir = os.path.join(os.getenv("HOME"), ".trage/problem/user")
        files = os.listdir(prob_dir)
        files.sort()
        for directory in files:
            if os.path.isdir(os.path.join(prob_dir, directory)):
                prob = Problem('user', directory)
                prob.load()
                self.model.append( [directory, prob.get_name(), prob.get_title()] )

    def init_treeview(self):
        self.treeview = self.builder.get_object('treeview_prob')

        # Create model
        self.model = gtk.ListStore(
                            gobject.TYPE_STRING,
                            gobject.TYPE_STRING,
                            gobject.TYPE_STRING)

        self.treeview.set_model(self.model)

        column = gtk.TreeViewColumn(_('ID'), gtk.CellRendererText(), text = COLUMN_ID)
        self.treeview.append_column(column)

        column = gtk.TreeViewColumn(_('Name'), gtk.CellRendererText(), text = COLUMN_NAME)
        self.treeview.append_column(column)

        column = gtk.TreeViewColumn(_('Title'), gtk.CellRendererText(), text = COLUMN_TITLE)
        self.treeview.append_column(column)

        self.update_model()

    def refresh(self, widget, data = None):
        """refresh - refresh the problem list"""
        self.update_model()

    def on_row_changed(self, widget, data = None):
        selection = self.treeview.get_selection()
        iter = selection.get_selected()[1]
        if iter:
            self.button_delete.set_sensitive(1)
            self.selected_prob_iter = iter
            self.selected_prob_id = self.model.get_value(iter, COLUMN_ID)

    def delete(self, widget, data = None):
        """delete - delete a problem"""
        # Delete dir
        self.button_delete.set_sensitive(0)
        prob_dir = os.path.join(os.getenv("HOME"), ".trage/problem/user", str(self.selected_prob_id))
        shutil.rmtree(prob_dir)

        # Delete row
        self.model.remove(self.selected_prob_iter)
        

    def quit(self, widget):
        """quit - signal handler for closing the AddDialog"""
        self.destroy()

    def on_destroy(self, widget):
        """on_destroy - called when the AddDialog is close"""
        gtk.main_quit()

if __name__ == "__main__":
    dialog = ManageDialog()
    dialog.show()
    gtk.main()
