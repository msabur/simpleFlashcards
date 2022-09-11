import os
import sys
import pathlib
from appdirs import user_data_dir
import tkinter as tk
from tkinter import ttk, filedialog
from ttkthemes import ThemedTk
import awesometkinter as atk
from awesometkinter.bidirender import add_bidi_support
from cardDeck import CardDeck
import cardParser

def resource_path(filename):
    base_path = getattr(sys, '_MEIPASS',
            os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, filename)

### global variables
###

def cardNumString(deck):
    """make a nice string with the current card number, e.g. 4/7"""
    cardNumber = deck.get_number() + 1 # making it 1-indexed
    numCards = deck.get_card_count()
    return f"{cardNumber}/{numCards}"


# https://stackoverflow.com/a/62485627
class WrappingLabel(tk.Label):
    '''a type of Label that automatically adjusts the wrap to the size'''
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.bind('<Configure>', lambda e: self.config(wraplength=self.winfo_width()))

class App(ThemedTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Simple Flashcards")
        self.geometry('450x250')
        self.iconphoto(False, tk.PhotoImage(file=resource_path('icon.gif')))
        self.protocol('WM_DELETE_WINDOW', self.on_close_clicked)

        self.deck = CardDeck()
        self.data_dir = user_data_dir('simple-flashcards')
        pathlib.Path(self.data_dir).mkdir(parents=True, exist_ok=True)

        self.addTopButtons()
        ttk.Separator(self, orient='horizontal').pack(fill=tk.X)

        self.mainLabel = WrappingLabel(self, anchor='n')
        self.mainLabel.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        add_bidi_support(self.mainLabel)
        self.mainLabel.set('Click Open to open a deck of flashcards.')

        ttk.Separator(self, orient='horizontal').pack(fill=tk.X)
        self.addStatusbar()
        self.addBottomButtons()
        self.setupShortcuts()

    def addTopButtons(self):
        topFrame = ttk.Frame(self)

        ttk.Button(topFrame, text="Open",
                command=self.show_filedialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(topFrame, text="Load last file",
                command=self.open_last_file).pack(side=tk.LEFT)
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
        self.mainLabel.set(self.deck.get_text())
        self.cardNumVar.set(cardNumString(self.deck))

    def open_last_file(self):
        savePath = os.path.join(self.data_dir, "lastFilename")
        if os.path.isfile(savePath):
            with open(savePath, 'r') as f:
                filename = f.read()
            if os.path.isfile(filename):
                self.open_file(filename)
                return

        self.safelyOpenDialog(tk.messagebox.showwarning,
                title="Last file not found",
                message="Last file not found. Try using Open")

    def open_file(self, filename):
        if filename:
            fronts, backs = cardParser.from_file(filename)
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
                savePath = os.path.join(self.data_dir, "lastFilename")
                with open(savePath, 'w') as f:
                    f.write(filename)

    def show_filedialog(self):
        filename = self.safelyOpenDialog(
                filedialog.askopenfilename
        )
        self.open_file(filename)

    def show_shortcuts(self):
        entries = [
                ('Shortcut', 'Action'),
                ('----', '----'),
                ('j', 'Next'),
                ('k', 'Previous'),
                ('f', 'Flip over'),
                ('s', 'Toggle shuffle'),
                ('r', 'Toggle reverse'),
                ('Ctrl-o', 'Open a flashcard file'),
                ('Ctrl-l', 'Load last file'),
                ('Ctrl-h', 'Show this window'),
        ]
        space = max([len(s[0]) for s in entries]) + 3
        message = '\n'.join([f"{combination: <{space}}{meaning}" for combination, meaning in entries])

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

        self.bind('<Control-o>', lambda _: self.show_filedialog())
        self.bind('<Control-l>', lambda _: self.open_last_file())
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
        # don't let root be closed before the dialog
        # this is to prevent an error
        self.close_enabled = False
        retval = dialog_function(*args, **kwargs)
        self.close_enabled = True
        return retval

    def report_callback_exception(self, exc, val, tb):
        print(f"{exc}, {val}, {tb}")
        self.safelyOpenDialog(
            tk.messagebox.showerror,
            title='Error',
            message=f'An error occurred: {exc.__name__}'
        )

    def on_close_clicked(self):
        if getattr(self, 'close_enabled', True):
            self.destroy()

if __name__ == '__main__':
    window = App(theme='breeze')
    window.mainloop()
