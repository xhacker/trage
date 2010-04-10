# -*- coding: utf-8 -*-

import gtk

import gettext
from gettext import gettext as _
gettext.textdomain('trage')

from trage.helpers import get_builder

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

        #code for other initialization actions should be added here
        self.tp = 1
        # 使减少测试点按钮不可用
        button_less = self.builder.get_object('button_tpless')
        button_less.set_sensitive(False)

    def tp_more(self, widget):
        '''增加一个测试点'''
        if self.tp == 1:
            # 使减少测试点按钮恢复可用
            button_less = self.builder.get_object('button_tpless')
            button_less.set_sensitive(True)
        self.tp += 1
        # add_row
        print self.tp

    def tp_less(self, widget):
        '''减少一个测试点'''
        if self.tp == 1:
            return

        # del_row
        self.tp -= 1
        if self.tp == 1:
            # 使减少测试点按钮不可用
            button_less = self.builder.get_object('button_tpless')
            button_less.set_sensitive(False)

        print self.tp

    def add(self, widget):
        pass

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
