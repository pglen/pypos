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

def str2float( col):
    return ( float(int(col[1:3], base=16)) / 256,
                    float(int(col[3:5], base=16)) / 256, \
                        float(int(col[5:7], base=16)) / 256 )


class LabelButt(Gtk.DrawingArea):

    def __init__(self, front, callb = None, toolt=""):
        Gtk.DrawingArea.__init__(self)

        self.bgcolor  = str2float("#bbbbbb")
        self.bgcolor2 = str2float("#aaaaaa")
        self.fgcolor  = str2float("#333333")
        self.bgcolor3 = str2float("ccccccc")

        self.pressed  = False
        self.callb = callb

        fsize = 20
        #fname = "Monospace"
        fontname = "Courier"

        self.setfont(fontname, fsize)
        self.add_events(Gdk.EventMask.ALL_EVENTS_MASK)

        font = "Sans 15"
        #self.label.override_font(Pango.FontDescription(font))

        self.curve =  Gdk.Cursor(Gdk.CursorType.CROSSHAIR)
        self.arrow =  Gdk.Cursor(Gdk.CursorType.ARROW)

        self.text = front
        self.connect("draw", self.draw_event)

        if toolt:
            self.label.set_tooltip_text(toolt)

        self.mouse_in = False

        self.connect("button-press-event",   self.press, front)
        self.connect("button-release-event", self.rele, front)

        self.connect("enter-notify-event", self.area_enter)
        self.connect("leave-notify-event", self.area_leave)

    def press(self, arg, arg2, arg3):
        #print("pressed", arg, arg2, arg3);
        arg.pressed = True
        arg.queue_draw()

    def rele(self, arg, arg2, arg3):
        #print("rele", arg2);
        arg.pressed = False
        arg.queue_draw()
        if self.callb:
            self.callb(arg, arg2, arg3)

    def draw_event(self, pdoc, cr):

        rect = pdoc.get_allocation()
        #print("alloc", rect.width, rect.height)
        #print("ww ", rect.width, rect.height)

        #ctx = self.get_style_context()
        #fg_color = ctx.get_color(Gtk.StateFlags.NORMAL)

        if self.pressed:
            cr.set_source_rgba(*list(self.bgcolor3))
        elif self.mouse_in:
            cr.set_source_rgba(*list(self.bgcolor))
        else:
            cr.set_source_rgba(*list(self.bgcolor2))

        cr.rectangle( 0, 0, rect.width, rect.height)
        cr.fill()

        self.layout = PangoCairo.create_layout(cr)
        self.layout.set_font_description(self.fd)

        cr.set_source_rgba(*list(self.fgcolor))

        if "\n"in self.text:
            #print("multi")
            ypos = 0; layxx = []; layyy = []; laytxt = []
            for aa in self.text.split():
                self.layout.set_text(aa, len(aa))
                (pr, lr) = self.layout.get_extents()
                layxx.append(lr.width / Pango.SCALE)
                layyy.append(lr.height / Pango.SCALE)
                laytxt.append(aa)

            yyext = 0;
            for bb in layyy:
                yyext += bb

            cnt = 0
            for xx in layxx:
                self.layout.set_text(laytxt[cnt], len(laytxt[cnt]))
                yy = layyy[cnt]
                cr.move_to(rect.width / 2 - xx / 2, ypos + rect.height / 2 - yyext / 2)
                PangoCairo.show_layout(cr, self.layout)
                ypos += yy
                cnt += 1

        else:
            self.layout.set_text(self.text, len(self.text))
            (pr, lr) = self.layout.get_extents()
            xx = lr.width / Pango.SCALE; yy = lr.height / Pango.SCALE;

            cr.move_to(rect.width / 2 - xx / 2, rect.height / 2 - yy / 2)
            PangoCairo.show_layout(cr, self.layout)


        #cr.move_to(0, 0)
        #cr.line_to(rect.width, rect.height)

        #cr.move_to(rect.width, 0)
        #cr.line_to(0, rect.height)

        #cr.stroke()

        return rect.width


    def setfont(self, fam, size):

        self.fd = Pango.FontDescription()

        self.fd.set_family(fam)
        # Will not wotk right on the MAC if simple set_size used
        self.fd.set_absolute_size(size * Pango.SCALE)

        self.pangolayout = self.create_pango_layout("a")
        self.pangolayout.set_font_description(self.fd)

        #print("pc", dir(PangoCairo))
        #print()
        #fm = Pango.FontMap()
        #ccc = Pango.create_context(fm)
        # Get Pango steps
        #self.cxx, self.cyy = self.pangolayout.get_pixel_size()
        (pr, lr) = self.pangolayout.get_extents()
        #self.printrect("pix", pr)
        #self.printrect("log", lr)

        self.cxx = lr.width / Pango.SCALE; self.cyy = lr.height / Pango.SCALE

        # Get Pango tabs
        self.tabarr = Pango.TabArray(80, False)
        #for aa in range(self.tabarr.get_size()):
        #    self.tabarr.set_tab(aa, Pango.TAB_LEFT, aa * TABSTOP * self.cxx * Pango.SCALE)

        self.pangolayout.set_tabs(self.tabarr)
        ts = self.pangolayout.get_tabs()

        '''if ts != None:
            al, self.tabstop = ts.get_tab(1)
        self.tabstop /= self.cxx * Pango.SCALE'''

        # Also set stip offset
        self.strip = 4 * self.cxx + 8


    def area_motion(self, arg1, arg2):
        print("LabelButt Motion", arg1, arg2)
        pass

    def area_enter(self, arg1, arg2):
        #print("LabelButt enter", arg1, arg2)
        #arg1.modify_bg(Gtk.StateType.NORMAL, Gdk.Color(0xffff, 0xffff, 0xffff))
        arg1.mouse_in = True
        arg1.queue_draw()
        pass

    def area_leave(self, arg1, arg2):
        #print("LabelButt leave", arg2)
        arg1.mouse_in = False
        arg1.queue_draw()
        #arg1.modify_bg(Gtk.StateType.NORMAL, Gdk.Color(0xeeee, 0xeeee, 0xeeee))
        pass


class TouchButt(Gtk.HBox):

    def __init__(self, txt, callb, colx = None):

        Gtk.HBox.__init__(self, txt)

        self.lab = LabelButt(txt, callb)

        self.set_margin_top(2)
        self.set_margin_bottom(2)
        self.set_margin_start(2)
        self.set_margin_end(2)

        self.pack_start(self.lab, 1, 1, 0)

        #if colx == None:
        #    self.modify_bg(Gtk.StateType.NORMAL, Gdk.Color(randc(), randc(), randc()))
        #else:
        #    self.modify_bg(Gtk.StateType.NORMAL, col)
        #
        #if colx:
        #    self.modify_bg(Gtk.StateType.NORMAL, colx)
        #else:
        #    self.modify_bg(Gtk.StateType.NORMAL, Gdk.Color(0xffff, 0xffff, 0xffff))

        #self.modify_bg(Gtk.StateType.NORMAL, Gdk.Color(randc(), randc(), randc()))
        #self.modify_fg(Gtk.StateType.NORMAL, Gdk.Color(randc(), randc(), randc()))

