# -*- coding: utf-8 -*-

import gtk

import gettext
from gettext import gettext as _
gettext.textdomain('trage')

from trage import (
    AddDialog)
from trage.helpers import get_builder

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

        #code for other initialization actions should be added here

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
