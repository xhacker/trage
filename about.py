# -*- coding: utf-8 -*-

import gtk

class AboutTrageDialog(gtk.AboutDialog):
    __gtype_name__ = "AboutTrageDialog"

    def __init__(self):
        pass

    def finish_init(self, builder):
        self.builder = builder
        self.builder.connect_signals(self)

        #code for other initialization actions should be added here


def new_about():
    ui_filename = 'ui/about_dialog.glade'
    builder = gtk.Builder()
    builder.add_from_file(ui_filename)    
    dialog = builder.get_object("about_trage_dialog")
    dialog.finish_init(builder)
    return dialog


if __name__ == "__main__":
    dialog = new_about()
    dialog.show()
    gtk.main()
