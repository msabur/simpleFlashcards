import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog
from ttkthemes import ThemedTk
from cardDeck import CardDeck
import cardParser

def changeToSourceDirectory():
    base_path = getattr(sys, '_MEIPASS',
            os.path.dirname(os.path.abspath(__file__)))
    os.chdir(base_path)

### global variables
deck = CardDeck()
###

def cardNumString():
    """make a nice string with the current card number, e.g. 4/7"""
    cardNumber = deck.get_number() + 1 # making it 1-indexed
    numCards = deck.get_card_count()
    return f"{cardNumber}/{numCards}"

class App(ThemedTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Simple Flashcards")
        self.geometry('400x200')

        self.addTopMenu()

        self.cardVar = tk.StringVar()
        self.cardVar.set('No cards open. Go to File | Open to open a deck of flashcards.')
        self.mainLabel = ttk.Label(self, textvariable=self.cardVar, anchor='n')
        self.mainLabel.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.shuffled = tk.IntVar()
        self.shuffled.set(0)

        self.addStatusbar()
        self.addBottomButtons()

    def addTopMenu(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # create the file_menu
        file_menu = tk.Menu(
            menubar,
            tearoff=0
        )

        file_menu.add_command(
            label='Open',
            command=self.open_file
        )

        file_menu.add_command(
            label='Exit',
            command=self.destroy
        )

        # add the File menu to the menubar
        menubar.add_cascade(
            label="File",
            menu=file_menu
        )

        help_menu = tk.Menu(
            menubar,
            tearoff=0
        )

        help_menu.add_command(
            label='Shortcuts',
            command=self.show_shortcuts
        )

        help_menu.add_command(
            label='About',
            command=self.show_about
        )

        # add the Help menu to the menubar
        menubar.add_cascade(
            label="Help",
            menu=help_menu
        )

    def addStatusbar(self):
        self.cardNumVar = tk.StringVar();
        self.cardNumVar.set('0/0')
        self.statusFrame = ttk.Frame(self)
        self.numLabel = ttk.Label(self.statusFrame, textvariable=self.cardNumVar)
        self.shuffleToggle = ttk.Checkbutton(self.statusFrame,
                text='Shuffle', variable=self.shuffled, onvalue=1,
                offvalue=0, command=self.doAndUpdate(deck.toggle_shuffle))

        self.statusFrame.pack(fill=tk.X)
        self.numLabel.pack(side=tk.LEFT)
        self.shuffleToggle.pack(side=tk.RIGHT)

    def addBottomButtons(self):
        self.prev_btn = ttk.Button(self, text="Previous")
        self.prev_btn['command'] = self.doAndUpdate(deck.prev_card)
        self.prev_btn.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.flip_btn = ttk.Button(self, text="Flip over")
        self.flip_btn['command'] = self.doAndUpdate(deck.flip)
        self.flip_btn.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.next_btn = ttk.Button(self, text="Next")
        self.next_btn['command'] = self.doAndUpdate(deck.next_card)
        self.next_btn.pack(side=tk.LEFT, fill=tk.X, expand=True)

    def updateCardView(self):
        self.cardVar.set(deck.get_text())
        self.cardNumVar.set(cardNumString())

    def open_file(self):
        filetypes = (
            ('text files', '*.txt'),
            ('All files', '*.*')
        )
        file = filedialog.askopenfile(filetypes=filetypes)

        if file:
            self.shuffled.set(0)
            deck.reset()
            fronts, backs = cardParser.from_string(file.read())
            deck.load_data(fronts, backs)
            self.updateCardView()

    def show_about(self):
        pass

    def show_shortcuts(self):
        pass

    def doAndUpdate(self, f):
        # for event handlers where we need to do something then update the view
        def inner():
            f()
            self.updateCardView()
        return inner

if __name__ == '__main__':
    changeToSourceDirectory()
    window = App(theme='arc')
    window.mainloop()

    # restart when closed. for developing only
    # TODO remove
    python = sys.executable
    os.execl(python, python, *sys.argv)
