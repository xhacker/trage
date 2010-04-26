# -*- coding: utf-8 -*-

import gtk

import gettext
from gettext import gettext as _
gettext.textdomain('trage')

from trage.helpers import get_builder

(
    LABEL,
    INFILE,
    ANSFILE,
    TIMELIMIT,
    MEMLIMIT,
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
        self.tp = 0
        self.tp_max = 0
        self.tp_widget_table = [[]]
        self.tp_more(None)

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

        # Add row
        if self.tp <= self.tp_max:
            self.tp_widget_table[self.tp][LABEL].set_visible(True)
            self.tp_widget_table[self.tp][INFILE].set_visible(True)
            self.tp_widget_table[self.tp][ANSFILE].set_visible(True)
            self.tp_widget_table[self.tp][TIMELIMIT].set_visible(True)
            self.tp_widget_table[self.tp][MEMLIMIT].set_visible(True)
        else:
            self.tp_max = self.tp
            table_tp = self.builder.get_object('table_tp')

            tp_widget_row = []
            # Add label
            label = gtk.Label(self.tp)
            label.show()
            tp_widget_row.append(label)
            table_tp.attach(label, LABEL, LABEL + 1, self.tp, self.tp + 1, xoptions=gtk.FILL)
            # Add input file chooser
            infile = gtk.FileChooserButton(_('Select Input File'))
            infile.show()
            tp_widget_row.append(infile)
            table_tp.attach(infile, INFILE, INFILE + 1, self.tp, self.tp + 1)
            # Add anwser file chooser
            ansfile = gtk.FileChooserButton(_('Select Answer File'))
            ansfile.show()
            tp_widget_row.append(ansfile)
            table_tp.attach(ansfile, ANSFILE, ANSFILE + 1, self.tp, self.tp + 1)
            # Add time limit spin button
            timelimit = gtk.SpinButton(adjustment = self.builder.get_object('adj_time'), digits = 1)
            timelimit.set_range(0.5, 20.0)
            timelimit.get_adjustment().set_step_increment(0.5)
            timelimit.show()
            tp_widget_row.append(timelimit)
            table_tp.attach(timelimit, TIMELIMIT, TIMELIMIT + 1, self.tp, self.tp + 1, xoptions=gtk.FILL)
            # Add mem limit spin button
            memlimit = gtk.SpinButton(adjustment = self.builder.get_object('adj_mem'))
            memlimit.set_range(2, 512)
            memlimit.get_adjustment().set_step_increment(2)
            memlimit.show()
            tp_widget_row.append(memlimit)
            table_tp.attach(memlimit, MEMLIMIT, MEMLIMIT + 1, self.tp, self.tp + 1, xoptions=gtk.FILL)

            self.tp_widget_table.append(tp_widget_row)

    def tp_less(self, widget):
        '''减少一个测试点'''
        if self.tp == 1:
            return

        # Delete row
        self.tp_widget_table[self.tp][LABEL].set_visible(False)
        self.tp_widget_table[self.tp][INFILE].set_visible(False)
        self.tp_widget_table[self.tp][ANSFILE].set_visible(False)
        self.tp_widget_table[self.tp][TIMELIMIT].set_visible(False)
        self.tp_widget_table[self.tp][MEMLIMIT].set_visible(False)

        self.tp -= 1

        if self.tp == 1:
            # 使减少测试点按钮不可用
            button_less = self.builder.get_object('button_tpless')
            button_less.set_sensitive(False)

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
