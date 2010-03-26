# -*- coding: utf-8 -*-

import gtk

class AddDialog(gtk.Window):
    __gtype_name__ = "AddDialog"

    def __init__(self):
        pass

    def finish_init(self, builder):
        self.builder = builder
        self.builder.connect_signals(self)

        #code for other initialization actions should be added here


    def quit(self, widget):
        """quit - signal handler for closing the AddDialog"""
        self.destroy()


    def on_destroy(self, widget):
        """on_destroy - called when the AddDialog is close"""
        gtk.main_quit()


def new_add():
    ui_filename = 'ui/add_dialog.glade'
    builder = gtk.Builder()
    builder.add_from_file(ui_filename)    
    dialog = builder.get_object("add_dialog")
    dialog.finish_init(builder)
    return dialog

if __name__ == "__main__":
    dialog = new_add()
    dialog.show()
    gtk.main()

