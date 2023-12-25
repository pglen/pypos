#!/usr/bin/env python

import os, sys, getopt, signal, select, random

import gi;
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import GLib
from gi.repository import Pango

gi.require_version('PangoCairo', '1.0')

from gi.repository import PangoCairo

gui_testmode = 0


def randc():
    return random.random() * 0xffff

        #ccc = Gdk.Color(randc(), randc(), randc())

def randcolstr(start = 0, endd = 255):
    rr =  random.randint(start, endd)
    gg =  random.randint(start, endd)
    bb =  random.randint(start, endd)
    strx = "#%02x%02x%02x" % (rr, gg, bb)
    return strx

class xSpacer(Gtk.HBox):

    def __init__(self, sp = None):
        GObject.GObject.__init__(self)
        #self.pack_start()
        if gui_testmode:
            col = randcolstr() #100, 200)
            print("xSpacer", col)
            self.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse(col))
        if sp == None:
            sp = 6
        self.set_size_request(sp, sp)


