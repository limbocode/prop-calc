from gi.repository import Gtk, Pango
from prop import Prop

class TextViewWindow(Gtk.Window):

    def __init__(self):
        self.prop = Prop()
        Gtk.Window.__init__(self, title="Prop Calc")

        self.set_default_size(350, 350)

        self.grid = Gtk.Grid()
        
        self.create_grid()
        self.add(self.grid)
        self.create_textview()

        self.create_label()
#        self.create_toolbar()
#        self.create_buttons()

    def create_grid(self):
        confirm_button = Gtk.Button(label="Confirm Validity")
        save_button = Gtk.Button(label="Save")
        load_button = Gtk.Button(label="Load")

        map(self.grid.add, [confirm_button, save_button, load_button])

        confirm_button.connect("clicked", self.confirm_click)
        save_button.connect("clicked", self.save_click)
        load_button.connect("clicked", self.load_click)
    
    def create_textview(self):
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        self.grid.attach(scrolledwindow, 0, 1, 3, 1)

        self.textview = Gtk.TextView()
        self.textbuffer = self.textview.get_buffer()
        scrolledwindow.add(self.textview)

    def create_label(self):
        self.label = Gtk.Label()
        self.label.set_text("")
        self.grid.attach(self.label,0,2,1,1)

    def confirm_click(self, button):
        f = open('temp.txt','w')
        i = self.textbuffer.get_start_iter()
        x = self.textbuffer.get_end_iter()
        f.write(self.textbuffer.get_text(i,x,True))
        f.close()
        f = open('temp.txt','r')
        if self.prop.confirm_validity(f):
            self.label.set_text("Valid")
        else:
            self.label.set_text("Is not Valid")

    def save_click(self, button):
        try:
            file1 = self.file_chooser_save()
            print file1
            if file1:
                f = open(file1,'w')
                i = self.textbuffer.get_start_iter()
                x = self.textbuffer.get_end_iter()
                f.write(self.textbuffer.get_text(i,x,True))
                f.close()
        except:
            pass

    def load_click(self, button):
        try:
            file1 = self.file_chooser_load()
            if file1:
                self.textbuffer.set_text(open(file1).read())
        except:
            pass

    def file_chooser_save(self):
        chooser = Gtk.FileChooserDialog("Save", self,
            Gtk.FileChooserAction.SAVE,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_SAVE, Gtk.ResponseType.OK))

        if chooser.run() == Gtk.ResponseType.OK:
            file1 = chooser.get_filename()

        chooser.destroy()
        
        if file1:
            return file1
        return None

    def file_chooser_load(self):
        chooser = Gtk.FileChooserDialog("Load", self,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        if chooser.run() == Gtk.ResponseType.OK:
            file1 = chooser.get_filename()

        chooser.destroy()
        if file1:
            return file1
        return None


if __name__ == "__main__":
    win = TextViewWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()
