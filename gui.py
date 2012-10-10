from gi.repository import Gtk, Pango
import prop

class TextViewWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="TextView Example")

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
        self.label.set_text("True")
        self.grid.attach(self.label,0,2,1,1)

    def confirm_click(self, button):
        f = open('temp.txt','w')
        i = self.textbuffer.get_start_iter()
        x = self.textbuffer.get_end_iter()
        f.write(self.textbuffer.get_text(i,x,True))
        f.close()
        self.label.set_text("False")

    def save_click(self, button):
        file1 = file_chooser()
        if file1:
            f = open('test.txt','w')
            i = self.textbuffer.get_start_iter()
            x = self.textbuffer.get_end_iter()
            f.write(self.textbuffer.get_text(i,x,True))
            f.close()


    def file_chooser(self):
        dialog = Gtk.FileChooserDialog("Please choose a file", self,
            Gtk.FileChooserAction.SAVE,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_SAVE, Gtk.ResponseType.OK))

        if dialog.run() == Gtk.ResponseType.OK:
            file1 = dialog.get_filename()

        dialog.destroy()
        if file1:
            return file1
        return None


win = TextViewWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
