# ------------------------------------------------------------------------
#

class BarWin():

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
        window.set_position(Gtk.WindowPosition.CENTER)
        if www > 2 * hhh:
            www = 6 * hhh / 3
        window.set_default_size(3*www/4, 3*hhh/4)
        #window.set_default_size(800, 600)
        #window.set_flags(Gtk.CAN_FOCUS | Gtk.SENSITIVE)
        window.connect("destroy", OnExit)

        vbox = Gtk.VBox();

        butt1 = Gtk.Button.new_with_mnemonic(" E_xit ")
        butt1.connect("clicked", self.click_ok, window)
        vbox.pack_end(butt1, 0, 0, False)

        self.vspacer(vbox)
        vbox.pack_start(self.header("  Bar Code:"), 0, 0, False )
        self.vspacer(vbox)

        hbox = Gtk.HBox();
        vbox.pack_start(hbox, 0, 0, False)
        self.barcode = Gtk.Entry();
        self.spacer(hbox)
        hbox.add(self.barcode)
        self.spacer(hbox)

        self.vspacer(vbox)
        vbox.pack_start(self.header("  Item:"), 0, 0, False )
        self.vspacer(vbox)

        hbox4 = Gtk.HBox();
        vbox.pack_start(hbox4, 0, 0, False)
        self.item = Gtk.Entry();
        self.spacer(hbox4)
        hbox4.add(self.item)
        self.spacer(hbox4)

        self.vspacer(vbox)
        vbox.pack_start(self.header("  Description:"), 0, 0, False )
        self.vspacer(vbox)

        hbox5 = Gtk.HBox();
        self.desc = Gtk.TextView();
        self.desc.set_border_width(8)

        sw = Gtk.ScrolledWindow()
        sw.add(self.desc)
        sw.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        sw.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.spacer(hbox5)
        hbox5.add(sw)
        vbox.pack_start(hbox5, 1, 1, False)
        self.spacer(hbox5)

        # ---------------------------------------------------------------
        window.add(vbox)
        window.show_all()

    def click_ok(self, win, aa):
        Gtk.main_quit()
        pass

    def header(self, xstr):
        lab3 = Gtk.Label(label=xstr)
        hbox3 = Gtk.HBox(); hbox3.pack_start(lab3, 0, 0, False )
        return hbox3

    def spacer(self, hbox, xstr = "    "):
        lab = Gtk.Label(label=xstr)
        hbox.pack_start(lab, 0, 0, False )

    def vspacer(self, vbox):
        lab = Gtk.Label(label=" ")
        vbox.pack_start(lab, 0, 0, False )

    def newcode(self, line):
        self.barcode.set_text(line)
        print(posdb.get(line))
        self.item.set_text("This is item '" + line + "'")



