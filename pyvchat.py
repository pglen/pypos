#!/usr/bin/env python

import os, sys, getopt, signal, select
import gobject, gtk, pango, gst
    
class VideoChat():    
    
    def __init__(self):

        win = Gtk.Window()
        win.set_resizable(False)
        win.set_has_frame(False)
        win.set_position(Gtk.WindowPosition.CENTER)

        fixed = Gtk.Fixed()
        win.add(fixed)
        fixed.show()

        self.videowidget = videowidget = Gtk.DrawingArea()
        fixed.put(videowidget, 0, 0)
        videowidget.set_size_request(640, 480)
        videowidget.show()

        # Setup GStreamer 
        self.player = player = Gst.ElementFactory.make("playbin", "MultimediaPlayer")
        bus = player.get_bus() 
        bus.add_signal_watch() 
        bus.enable_sync_message_emission() 
        #used to get messages that GStreamer emits 
        bus.connect("message", self.on_message) 
        #used for connecting video to your application 
        bus.connect("sync-message::element", self.on_sync_message)
        
        #player.set_property("uri", "file://" + os.getcwd() + "/VID/SEQ-GAME-OPEN.ogv") 
        player.set_property("uri", "file://" +  
            os.getcwd() + "/aa.ogv")
            #"/home/peterglen/pgsrc/pygtk/pypos/pypos-001/aa.ogv")
            #"/home/peterglen/usb_old/Videos/Webcam/2014-04-15-212010.ogv")
            #"/home/peterglen/rpmbuild/SOURCES/g/gst-python-0.10.16/examples/aa.ogv") 

        player.set_state(Gst.State.PLAYING)

        win.show()

    def on_message(self, bus, message): 
        #print "player message", message
        if message.type == Gst.MessageType.EOS: 
            # End of Stream 
            self.player.set_state(Gst.State.NULL) 
        elif message.type == Gst.MessageType.ERROR: 
            self.player.set_state(Gst.State.NULL) 
            (err, debug) = message.parse_error() 
            print("Error: %s" % err, debug)

    def on_sync_message(self, bus, message):
        print("player sync message", message)
        if message.structure is None: 
            return False 
        if message.structure.get_name() == "prepare-xwindow-id":
            '''if sys.platform == "win32":
                win_id = self.videowidget.window.handle
            else:
                win_id = self.videowidget.window.xid
            assert win_id
            imagesink = message.src 
            imagesink.set_property("force-aspect-ratio", True)
            imagesink.set_xwindow_id(win_id) '''
            pass

if __name__ == '__main__':

    vc = VideoChat()    
    Gtk.main()



