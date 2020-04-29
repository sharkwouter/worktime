import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
from worktime.state import Track
import time


@Gtk.Template.from_file("data/ui/tracker.ui")
class Tracker(Gtk.Box):
    __gtype_name__ = "Tracker"

    button_break = Gtk.Template.Child()
    button_work = Gtk.Template.Child()
    button_procrastinate = Gtk.Template.Child()
    label_time = Gtk.Template.Child()
    label_break = Gtk.Template.Child()
    label_work = Gtk.Template.Child()
    label_procrastinate = Gtk.Template.Child()

    def __init__(self):
        Gtk.Box.__init__(self)
        self.start_time = time.time()
        self.previous_time = self.start_time
        self.tracking = Track.WORK
        self.timers = {str(Track.BREAK): 0, str(Track.WORK): 0, str(Track.PROCRASTINATE): 0}
        self.update_time()
        GLib.timeout_add_seconds(60, self.update_time)

    @Gtk.Template.Callback("change_tracked_time")
    def change_tracked_time(self, widget):
        if widget == self.button_break:
            self.tracking = Track.BREAK
        elif widget == self.button_procrastinate:
            self.tracking = Track.PROCRASTINATE
        elif widget == self.button_work:
            self.tracking = Track.WORK

    def update_time(self):
        time_now = time.time()
        time_delta = time.time() - self.previous_time
        self.previous_time = time_now
        self.timers[str(self.tracking)] += time_delta
        time_string = self.seconds_to_text(time_now - self.start_time)
        self.label_time.set_text(time_string)
        self.update_minor_timers()
        GLib.timeout_add_seconds(60, self.update_time)

    def seconds_to_text(self, seconds):
        hours = int(seconds / 3600)
        minutes = int((seconds % 3600) / 60)
        time_string = "{:02d}:{:02d}".format(hours, minutes)
        return time_string

    def minutes_to_text(self, minutes):
        return self.seconds_to_text(minutes*60)

    def update_minor_timers(self):
        self.label_break.set_text(self.seconds_to_text(self.timers[str(Track.BREAK)]))
        self.label_work.set_text(self.seconds_to_text(self.timers[str(Track.WORK)]))
        self.label_procrastinate.set_text(self.seconds_to_text(self.timers[str(Track.PROCRASTINATE)]))
