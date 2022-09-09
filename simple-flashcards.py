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
###

def cardNumString(deck):
    """make a nice string with the current card number, e.g. 4/7"""
    cardNumber = deck.get_number() + 1 # making it 1-indexed
    numCards = deck.get_card_count()
    return f"{cardNumber}/{numCards}"


# https://stackoverflow.com/a/62485627
class WrappingLabel(ttk.Label):
    '''a type of Label that automatically adjusts the wrap to the size'''
    def __init__(self, master=None, **kwargs):
        ttk.Label.__init__(self, master, **kwargs)
        self.bind('<Configure>', lambda e: self.config(wraplength=self.winfo_width()))

class App(ThemedTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Simple Flashcards")
        self.geometry('450x250')
        self.iconphoto(False, tk.PhotoImage(file='icon.png'))
        self.deck = CardDeck()

        self.addTopButtons()
        ttk.Separator(self, orient='horizontal').pack(fill=tk.X)

        self.cardVar = tk.StringVar()
        self.cardVar.set('Click Open to open a deck of flashcards.')
        self.mainLabel = WrappingLabel(self, textvariable=self.cardVar,
                anchor='n')
        self.mainLabel.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


        ttk.Separator(self, orient='horizontal').pack(fill=tk.X)
        self.addStatusbar()
        self.addBottomButtons()
        self.setupShortcuts()

    def addTopButtons(self):
        topFrame = ttk.Frame(self)

        ttk.Button(topFrame, text="Open",
                command=self.open_file).pack(side=tk.LEFT)
        ttk.Button(topFrame, text="Shortcuts",
                command=self.show_shortcuts).pack(side=tk.RIGHT)

        topFrame.pack(fill=tk.X)

    def addStatusbar(self):
        self.cardNumVar = tk.StringVar();
        self.cardNumVar.set('0/0')
        self.shuffled = tk.IntVar()
        self.shuffled.set(0)
        self.reversed = tk.IntVar()
        self.reversed.set(0)

        statusFrame = ttk.Frame(self)
        numLabel = ttk.Label(statusFrame,
                textvariable=self.cardNumVar)
        shuffleToggle = ttk.Checkbutton(statusFrame,
                text='Shuffle', variable=self.shuffled, onvalue=1,
                offvalue=0,
                command=self.cardCb(self.deck.toggle_shuffle))
        reverseToggle = ttk.Checkbutton(statusFrame,
                text='Reverse', variable=self.reversed, onvalue=1,
                offvalue=0,
                command=self.cardCb(self.deck.toggle_reverse))

        statusFrame.pack(fill=tk.X)
        numLabel.pack(side=tk.LEFT)
        shuffleToggle.pack(side=tk.RIGHT)
        reverseToggle.pack(side=tk.RIGHT)

    def addBottomButtons(self):
        prev_btn = ttk.Button(self, text="Previous")
        prev_btn['command'] = self.cardCb(self.deck.prev_card)
        prev_btn.pack(side=tk.LEFT, fill=tk.X, expand=True)

        flip_btn = ttk.Button(self, text="Flip over")
        flip_btn['command'] = self.cardCb(self.deck.flip)
        flip_btn.pack(side=tk.LEFT, fill=tk.X, expand=True)

        next_btn = ttk.Button(self, text="Next")
        next_btn['command'] = self.cardCb(self.deck.next_card)
        next_btn.pack(side=tk.LEFT, fill=tk.X, expand=True)

    def updateCardView(self):
        if not self.deck.loaded: return # to preserve placeholder texts
        self.cardVar.set(self.deck.get_text())
        self.cardNumVar.set(cardNumString(self.deck))

    def open_file(self):
        filetypes = (
            ('text files', '*.txt'),
            ('All files', '*.*')
        )
        file = self.safelyOpenDialog(
                filedialog.askopenfile,
                filetypes=filetypes
        )

        if file:
            fronts, backs = cardParser.from_string(file.read())
            if fronts is None:
                # not using exceptions because try/catch is weird on tkinter
                self.safelyOpenDialog(tk.messagebox.showerror,
                        title="Parsing error",
                        message="Please check the format of the flashcards file")
            else:
                self.shuffled.set(0)
                self.reversed.set(0)
                self.deck.reset()
                self.deck.load_data(fronts, backs)
                self.updateCardView()

    def show_shortcuts(self):
        shortcuts = [
                ('j', 'Next'),
                ('k', 'Previous'),
                ('f', 'Flip over'),
                ('s', 'Toggle shuffle'),
                ('r', 'Toggle reverse'),
                ('Ctrl-o', 'Open a flashcard file'),
                ('Ctrl-h', 'Show this window'),
        ]
        space = max([len(s[0]) for s in shortcuts]) + 5
        message = '\n'.join([f"{combination: <{space}}{meaning}" for combination, meaning in shortcuts])

        self.option_add('*Dialog.msg.font', "Monospace 10")
        self.grab_set()
        self.safelyOpenDialog(
            tk.messagebox.showinfo,
            title='Shortcuts',
            message=message
        )
        self.option_clear()

    def setupShortcuts(self):
        flipVar = lambda v: v.set(1 if v.get() == 0 else 0)
        def toggle_shuffle():
            flipVar(self.shuffled)
            self.deck.toggle_shuffle()

        def toggle_reverse():
            flipVar(self.reversed)
            self.deck.toggle_reverse()

        self.bind('<Control-o>', lambda _: self.open_file())
        self.bind('<Control-h>', lambda _: self.show_shortcuts())
        self.bind('s', lambda _: self.cardCb(toggle_shuffle)())
        self.bind('r', lambda _: self.cardCb(toggle_reverse)())
        self.bind('j', lambda _: self.cardCb(self.deck.next_card)())
        self.bind('k', lambda _: self.cardCb(self.deck.prev_card)())
        self.bind('f', lambda _: self.cardCb(self.deck.flip)())

    def cardCb(self, f):
        # returns a callback function that calls "f" then updates the view
        def inner():
            f()
            self.updateCardView()
        return inner

    def safelyOpenDialog(self, dialog_function, *args, **kwargs):
        # keeps the root hidden while the dialog is open.
        # this prevents errors if the root is closed before the dialog.
        self.withdraw()
        retval = dialog_function(*args, **kwargs)
        self.deiconify()
        return retval

    def report_callback_exception(self, exc, val, tb):
        print(f"{exc}, {val}, {tb}")
        self.safelyOpenDialog(
            tk.messagebox.showerror,
            title='Error',
            message=f'An error occurred: {exc.__name__}'
        )

if __name__ == '__main__':
    changeToSourceDirectory()
    window = App(theme='breeze')
    window.mainloop()
