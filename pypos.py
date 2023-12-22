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

import pypossql
from touchbutt import *

gui_testmode = 0
tbarr = []
# ------------------------------------------------------------------------
# This is open source sticker program. Written in python.

GAP = 4                 # Gap in pixels
TABSTOP = 4
FGCOLOR  = "#000000"
BGCOLOR  = "#ffff88"

sdev = "/dev/ttyS0"
fd = None

version = 1.0
verbose = False

# Where things are stored (backups, orgs, macros)
config_dir = os.path.expanduser("~/.pypos")

def randc():
    return random.random() * 0xffff

class xSpacer(Gtk.HBox):

    def __init__(self, sp = None):
        GObject.GObject.__init__(self)
        #self.pack_start()
        if gui_testmode:
            col = randcolstr(100, 200)
            self.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse(col))
        if sp == None:
            sp = 6
        self.set_size_request(sp, sp)


class TouchWin():

    def __init__(self):

        disp2 = Gdk.Display()
        disp = disp2.get_default()
        #print( disp)
        scr = disp.get_default_screen()
        ptr = disp.get_pointer()
        mon = scr.get_monitor_at_point(ptr[1], ptr[2])
        geo = scr.get_monitor_geometry(mon)
        www = geo.width; hhh = geo.height
        xxx = geo.x;     yyy = geo.y

        # Resort to old means of getting screen w / h
        if www == 0 or hhh == 0:
            www = Gdk.screen_width(); hhh = Gdk.screen_height()

        #www = Gdk.Screen.width(); hhh = Gdk.Screen.height();
        window = Gtk.Window.new(Gtk.WindowType.TOPLEVEL)
        #window = Gtk.Window.new(Gtk.WindowType.POPUP)
        window.set_position(Gtk.WindowPosition.CENTER)

        window.set_events(Gdk.EventMask.ALL_EVENTS_MASK )
        window.set_accept_focus(True)
        window.activate_focus()
        window.set_decorated(0)
        #window.set_default_size(3*www/4, 3*hhh/4)
        window.set_default_size(www, hhh)

        window.set_focus_on_map(True)
        window.connect("destroy", OnExit)

        vbox = Gtk.VBox();
        hbox = Gtk.HBox();

        vbox2 = Gtk.VBox();vbox3 = Gtk.VBox(); vbox4 = Gtk.VBox()

        hbox.pack_start(Gtk.Label.new("  "), 0,0,0);
        hbox.pack_start(vbox2, 1,1,0);
        hbox.pack_start(Gtk.Label.new("      "), 0,0,0);
        hbox.pack_start(vbox3, 1,1,0);
        hbox.pack_start(Gtk.Label.new("      "), 0,0,0);
        hbox.pack_start(vbox4, 1,1,0);
        hbox.pack_start(Gtk.Label.new("  "), 0,0,0);

        vbox.pack_start(Gtk.Label.new(" "), 0,0,0);
        vbox.pack_start(hbox, 1, 1, False)
        vbox.pack_start(Gtk.Label.new(" "), 0,0,0);

        # Left row -----------------------------------------------------
        ccc = Gdk.Color(0xeeee, 0xeeee, 0xeeee)

        for aa in range(6):
            hbox2 = Gtk.HBox()
            hbox2.set_homogeneous(True)
            for bb in range(4):
                tb = TouchButt("Hello\n%d %d" % (aa, bb), self.callb, ccc)
                hbox2.pack_start(tb, 1, 1, 0)

            vbox2.pack_start(hbox2, 1, 1, 0)
            if aa == 0:
                vbox2.pack_start(Gtk.Label.new(" "), 0,0,0);

        textx = [1,2,3,4]
        textx[0] = ["1 ", "2 ", "3 ", "+ "]
        textx[1] = ["4 ", "5 ", "6 ", "= "]
        textx[2] = ["7 ", "8 ", "9 ", "* "]
        textx[3] = ["  ", "0", "  ", "= "]

        # Middle row -----------------------------------------------------
        vbox33 = Gtk.VBox()
        vbox333 = Gtk.VBox()

        self.topmid = Gtk.TextView()
        vbox33.pack_start(self.topmid, 1, 1, 0)
        vbox33.pack_start(Gtk.Label.new(" "), 0, 0, 0)

        #ccc = Gdk.Color(randc(), randc(), randc())
        ccc = Gdk.Color(0xdddd, 0xdddd, 0xdddd)

        for aa in range(4):
            hbox2 = Gtk.HBox()
            hbox2.set_homogeneous(True)
            for bb in range(4):
                tb = TouchButt(textx[aa][bb], self.calb, ccc)
                #tb = TouchButt("Calc %d %d" % (aa, bb), self.calb)
                tbarr.append(tb)

                hbox2.pack_start(tb, 1, 1, 0)
            vbox333.pack_start(hbox2, 1, 1, 0)
        vbox33.pack_start(vbox333, 1, 1, 0)
        vbox3.pack_start(vbox33, 1, 1, 0)

        # Right row ------------------------------------------------------
        ccc = Gdk.Color(0xeeee, 0xeeee, 0xeeee)

        vbox44 = Gtk.VBox()
        for aa in range(4):
            hbox2 = Gtk.HBox()
            for bb in range(4):
                tb = TouchButt("Result %d %d" % (aa, bb), self.callx, ccc)
                hbox2.pack_start(tb, 1, 1, 0)
            vbox44.pack_start(hbox2, 1, 1, 0)

        #vbox44.pack_start(Gtk.Label.new("BUTT "), 1, 1, 0)
        self.botright = Gtk.TextView()
        vbox44.pack_start(Gtk.Label.new(" "), 0, 0, 0)

        self.scrollx = Gtk.ScrolledWindow()
        self.scrollx.add(self.botright)
        vbox44.pack_start(self.scrollx, 1, 1, 0)

        vbox4.pack_start(vbox44, 1, 1, 0)

        # End code for rows ------------------------------------------------------

        butt1 = Gtk.Button.new_with_mnemonic(" E_xit ")
        butt1.connect("clicked", self.click_ok, window)
        hboxe = Gtk.HBox()
        hboxe.pack_start(Gtk.Label.new(" "), 1, 1, 0)
        hboxe.pack_start(butt1, 0, 0, 0)
        #hboxe.pack_start(Gtk.Label.new(" "), 0, 0, 0)
        vbox.pack_start(hboxe, 0, 0, False)
        vbox.pack_start(xSpacer(), 0, 0, False)

        #vbox.pack_start(Gtk.Label.new(" "), 0, 0, False)
        vbox.pack_start(xSpacer(), 0, 0, False)

        window.connect("motion-notify-event", self.win_area_motion)

        # ---------------------------------------------------------------
        window.add(vbox)
        window.show_all()

    def win_area_motion(self, area, event):
        #print("window motion event", event.get_state(), event.x, event.y)
        if event.get_state() & Gdk.ModifierType.BUTTON1_MASK:
            print("drag",  event.x, event.y)

    def calb(self, win, arg1, arg2):
        #print("calb", win, arg1, arg2)
        self.logx(arg2)
        pass

    def callb(self, win, arg1, arg2):
        #print("callb", win, arg1, arg2)
        self.logx(arg2)
        pass

    def callx(self, win, arg1, arg2):
        #print("callx", win, arg1, arg2)
        self.logx(arg2)
        pass

    def logx(self, arg2):

        tb = self.botright.get_buffer()
        ttt = tb.get_text(tb.get_start_iter(), tb.get_end_iter(), False)
        tb.set_text(ttt + arg2 + "\n")
        self.botright.scroll_to_iter(tb.get_end_iter(), 0, False, 1., 0)
        adj = self.scrollx.get_vadjustment()
        #adj.set_value(adj.get_upper() - adj.get_page_size())
        adj.set_value(adj.get_upper() )


    def click_ok(self, win, aa):
        Gtk.main_quit()
        pass

    def header(self, xstr):
        lab3 = Gtk.Label(label=xstr)
        hbox3 = Gtk.HBox(); hbox3.pack_start(lab3, 0, 0, False )
        return hbox3


    def newcode(self, line):
        self.barcode.set_text(line)
        print(posdb.get(line))
        self.item.set_text("This is item '" + line + "'")


def OnExit(win):
    Gtk.main_quit()

def help():

    print()
    print("Pypos version: ", version)
    print()
    print("Usage: " + os.path.basename(sys.argv[0]) + " [options] [[filename] ... [filenameN]]")
    print()
    print("Options:")
    print()
    print("            -d level  - Debug level 1-10. (Limited implementation)")
    print("            -v        - Verbose (to stdout and log)")
    print("            -c        - Dump Config")
    print("            -h        - Help")
    print()


def OpenSerial(*par):
    global fd, sdev
    #print("Using device:", sdev)
    try:
        fd = open (sdev, "rt", 1)
    except:
        print("cannot open ", sdev)
        return

    '''try:
        while True:
            line = fd.readline()
            print line
    except:
        print "ended exc"

    print "Ended thread"'''

# ------------------------------------------------------------------------

tick = 0

def handler_tick():

    global mainwin, fd, tick

    tick += 1

    #if tick % 10 == 0:
    #    print 'handler called', fd.fileno(), tick

    # See if file descriptor has data:
    sel = select.select( (fd,), (), (), 0)
    if sel[0]:
        #print sel
        line = fd.readline()
        #for aa in line:
        #    print ord(aa),
        #print

        line = line.replace("\r", "").replace("\n", "")
        #print line
        if line != "":
            mainwin.newcode(line)

    #GLib.timeout_add(100, handler_tick)

def refresh_screen():
    pass
    #print("refresh")
    #for aa in tbarr:
    #    aa.queue_draw()

    return True

# Start of program:

if __name__ == '__main__':

    global mainwin, posdb

    try:
        if not os.path.isdir(config_dir):
            os.mkdir(config_dir)
    except: pass

    # Let the user know it needs fixin'
    if not os.path.isdir(config_dir):
        print("Cannot access config dir:", config_dir)
        sys.exit(1)

    posdb = pypossql.Possql(config_dir + "/data")

    opts = []; args = []
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hv")
    except getopt.GetoptError as err:
        print("Invalid option(s) on command line:", err)
        sys.exit(1)

    #print "opts", opts, "args", args

    for aa in opts:
        if aa[0] == "-d":
            try:
                pgdebug = int(aa[1])
            except:
                pgdebug = 0

        if aa[0] == "-h": help();  exit(1)
        if aa[0] == "-v": verbose = True
        #if aa[0] == "-x": clear_config = True
        #if aa[0] == "-c": show_config = True
        #if aa[0] == "-t": show_timing = True

    if verbose:
        print("PyPos running on", "'" + os.name + "'", \
            "GTK", Gtk.gtk_version, "PyGtk", Gtk.pygtk_version)

    #OpenSerial()

    # Poll the serial port of the scanner
    #GLib.timeout_add(200, handler_tick)

    #mainwin = BarWin()
    mainwin = TouchWin()

    GLib.timeout_add(1000, refresh_screen)

    Gtk.main()

# EOF
