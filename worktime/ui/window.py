import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from worktime.state import State
from worktime.ui.tracker import Tracker


@Gtk.Template.from_file("data/ui/window.ui")
class Window(Gtk.ApplicationWindow):
    __gtype_name__ = "Window"

    headerbar = Gtk.Template.Child()
    button_start = Gtk.Template.Child()
    button_stop = Gtk.Template.Child()
    button_properties = Gtk.Template.Child()
    label_start = Gtk.Template.Child()

    def __init__(self):
        Gtk.ApplicationWindow.__init__(self)
        self.state = State.READY
        self.show_all()

    @Gtk.Template.Callback("on_button_start_clicked")
    def start(self, widget):
        self.state = State.RUNNING
        widget.hide()
        self.button_stop.show()
        self.remove(self.label_start)
        self.add(Tracker())

    @Gtk.Template.Callback("on_button_stop_clicked")
    def stop(self, widget):
        message_dialog = Gtk.MessageDialog(
            parent=self,
            flags=Gtk.DialogFlags.MODAL,
            message_type=Gtk.MessageType.WARNING,
            buttons=Gtk.ButtonsType.OK_CANCEL,
            message_format="Are you sure you wish to end the work day?"
        )
        response = message_dialog.run()

        if response == Gtk.ResponseType.OK:
            self.state = State.DONE
            widget.hide()
            self.button_start.show()
        message_dialog.destroy()

    @Gtk.Template.Callback("on_button_properties_clicked")
    def properties(self, widget):
        print("Showing properties")
