# -*- coding: utf-8 -*-

import gtk

from trage.helpers import get_builder

import gettext
from gettext import gettext as _
gettext.textdomain('trage')

class AboutDialog(gtk.AboutDialog):
    __gtype_name__ = "AboutDialog"

    def __new__(cls):
        """Special static method that's automatically called by Python when 
        constructing a new instance of this class.
        
        Returns a fully instantiated AboutFooDialog object.
        """
        builder = get_builder('AboutDialog')
        new_object = builder.get_object("about_dialog")
        new_object.finish_init(builder)
        return new_object

    def finish_init(self, builder):
        self.builder = builder
        self.builder.connect_signals(self)

        #code for other initialization actions should be added here

if __name__ == "__main__":
    dialog = AboutDialog()
    dialog.show()
    gtk.main()
