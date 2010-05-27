# -*- coding: utf-8 -*-

import gtk
import gobject
import os

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

        #code for other initialization actions
        self.init_treeview()

    def init_treeview(self):
        treeview = self.builder.get_object('treeview_prob')

        # create model
        model = gtk.ListStore(
                            gobject.TYPE_STRING,
                            gobject.TYPE_STRING,
                            gobject.TYPE_STRING)

        # TODO: move duplicate codes to common/problem.py (get_prob_list)
        prob_dir = os.path.join(os.getenv("HOME"), ".trage/problem/user")
        files = os.listdir(prob_dir)
        for directory in files:
            if os.path.isdir(os.path.join(prob_dir, directory)):
                prob = Problem('user', directory)
                prob.load()
                model.append( ( directory, prob.get_name(), prob.get_title() ) )

        treeview.set_model(model)

        column = gtk.TreeViewColumn(_('ID'), gtk.CellRendererText(), text = COLUMN_ID)
        treeview.append_column(column)

        column = gtk.TreeViewColumn(_('Name'), gtk.CellRendererText(), text = COLUMN_NAME)
        treeview.append_column(column)

        column = gtk.TreeViewColumn(_('Title'), gtk.CellRendererText(), text = COLUMN_TITLE)
        treeview.append_column(column)

    def add(self, widget, data=None):
        """add - display the add box for Trage"""
        add = AddDialog.AddDialog()
        add.show()

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
