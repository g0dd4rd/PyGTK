import subprocess

import gi
gi.require_version('Gdk', '3.0')
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit2', '4.0')
from gi.repository import Gdk, Gio, Gtk, WebKit2

class PopoverWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Popover Demo")
        self.set_border_width(10)
        self.set_default_size(640, 480)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        self.add(scrolledwindow)

        self.textview = Gtk.TextView()
        self.textview.set_editable(True)
        self.textview.set_wrap_mode(Gtk.WrapMode.WORD)
        self.textview.connect("button-release-event", self.on_text_selected)
        self.textbuffer = self.textview.get_buffer()
        self.textbuffer.set_text("This is some text inside of a Gtk.TextView. "
            + "Select text and click one of the buttons 'bold', 'italic', "
            + "or 'underline' to modify the text accordingly.")
        scrolledwindow.add(self.textview)

        self.popover = Gtk.Popover()
        vbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.dictionarymbtn = Gtk.ModelButton("Dictionary")
        self.dictionarymbtn.connect("button-press-event", self.dict_query)
        vbox.pack_start(self.dictionarymbtn, False, True, 10)
        self.gtranslate = Gtk.ModelButton("gTranslate")
        self.gtranslate.connect("button-press-event", self.gtranslate_query)
        vbox.pack_start(self.gtranslate, False, True, 10)
        self.popover.add(vbox)
        self.popover.set_position(Gtk.PositionType.BOTTOM)
        self.popover.set_constrain_to(Gtk.PopoverConstraint.NONE)

    def on_text_selected(self, bounds, widget):
        bounds = self.textbuffer.get_selection_bounds()
        if len(bounds) != 0:
            self.word = self.textbuffer.get_text(bounds[0], bounds[1], False)
            
            self.popover.set_relative_to(self.textview)
            rect_loc = self.textview.get_cursor_locations(bounds[0])
            self.popover.set_pointing_to(rect_loc[0])
            self.popover.show_all()
            self.popover.popup()

    def dict_query(self, widget, x):
        subprocess.run(["firefox", "--new-tab", "https://www.dictionary.com/browse/"+ self.word])

    def gtranslate_query(self, widget, y):
        subprocess.run(["firefox", "--new-tab", "https://translate.google.com/#view=home&op=translate&sl=en&tl=cs&text="+ self.word])

win = PopoverWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()

