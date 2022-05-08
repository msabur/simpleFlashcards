import os
import sys
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from cardDeck import CardDeck
import cardParser

base_path = getattr(sys, '_MEIPASS',
        os.path.dirname(os.path.abspath(__file__)))
os.chdir(base_path)

### global variables
builder = Gtk.Builder()

deck = CardDeck()
###


class SignalHandlers:
    def onDestroy(self, *args):
        Gtk.main_quit()

    def onCardChange(self, button):
        if not deck.loaded:
            # do nothing if the user hasn't opened flashcards yet
            return

        funcs = { 
                'backBtn': deck.prev_card,
                'flipOverBtn': deck.flip,
                'forwardBtn': deck.next_card
                }
        funcs[button.get_name()]()

        card_buffer = builder.get_object("cardTextBuffer")
        card_buffer.set_text(deck.get_text())

    def on_open_activate(self, _):
        dialog = builder.get_object("FileChooserDialog")
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            try:
                fronts, backs = cardParser.from_file(dialog.get_filename())
                deck.load_data(fronts, backs)
                card_buffer = builder.get_object("cardTextBuffer")
                card_buffer.set_text(deck.get_text())
            except Exception as e:
                print(e)
                error_dialog = builder.get_object("ParsingErrorDialog")
                error_dialog.run()
                # not doing anything with the response
                error_dialog.hide()

        dialog.hide()

    def on_about_activate(self, _):
        dialog = builder.get_object("AboutDialog")
        response = dialog.run()
        dialog.hide()


builder.add_from_file("design.glade")
builder.connect_signals(SignalHandlers())
window = builder.get_object("MainWindow")
window.show_all()
Gtk.main()
