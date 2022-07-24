import os
import sys
import traceback
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

def cardNumString():
    """make a nice string with the current card number, e.g. 4/7"""
    cardNumber = deck.get_number() + 1 # making it 1-indexed
    numCards = deck.get_card_count()
    return f"{cardNumber}/{numCards}"

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
                'forwardBtn': deck.next_card,
                'shuffleBtn': deck.toggle_shuffle,
                'reverseBtn': deck.toggle_reverse,
                }
        funcs[button.get_name()]()

        card_buffer = builder.get_object("cardTextBuffer")
        card_buffer.set_text(deck.get_text())

        cardNumBuf = builder.get_object("cardNumber").get_buffer()
        cardNumBuf.set_text(cardNumString())

    def on_open_activate(self, _):
        dialog = builder.get_object("FileChooserDialog")
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            try:
                # Load cards from the file
                fronts, backs = cardParser.from_file(dialog.get_filename())
                deck.load_data(fronts, backs)

                # Make the cards show up on screen
                card_buffer = builder.get_object("cardTextBuffer")
                card_buffer.set_text(deck.get_text())

                # Start in an unshuffled state
                shuffleBtn = builder.get_object('shuffleBtn')
                shuffleBtn.set_sensitive(True)
                shuffleBtn.set_active(False)

                # Start in an unreversed state
                reverseBtn = builder.get_object('reverseBtn')
                reverseBtn.set_sensitive(True)
                reverseBtn.set_active(False)

                # Show card number
                cardNumBuf = builder.get_object("cardNumber").get_buffer()
                cardNumBuf.set_text(cardNumString())
            except Exception as e:
                print(traceback.format_exc())
                error_dialog = builder.get_object("ParsingErrorDialog")
                error_dialog.run()
                # not doing anything with the response
                error_dialog.hide()

        dialog.hide()

    def on_about_activate(self, _):
        dialog = builder.get_object("AboutDialog")
        dialog.run()
        dialog.hide()

    def on_keyboardShortcuts_activate(self, _):
        dialog = builder.get_object("KeyboardShortcutsDialog")
        dialog.run()
        dialog.hide()


builder.add_from_file("design.glade")
builder.connect_signals(SignalHandlers())
window = builder.get_object("MainWindow")
window.show_all()
Gtk.main()
