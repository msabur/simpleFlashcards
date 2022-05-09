import random

"""A deck of flashcards"""
class CardDeck:
    def __init__(self):
        self.loaded = False # used for the GUI
        self.fronts = []
        self.backs = []
        self.current_card = 0
        self.is_flipped = False
        self.cardSequence = []
        self.shuffled = False

        # cardSequence stores indices like [0,1,2,3,..]
        # to shuffle cards, we randomize cardSequence: e.g. [3,2,4,1,...]
        # then we will access cards in that new order

    def load_data(self, fronts, backs):
        # Doing some input validation
        if not isinstance(fronts, list) or not isinstance(backs, list):
            raise ValueError("Invalid card data")
        elif len(fronts) != len(backs):
            raise ValueError("Invalid card data")
        else:
            self.shuffled = False
            self.clear_cards()
            for front, back in zip(fronts, backs):
                self.fronts.append(front)
                self.backs.append(back)
            self.loaded = True
            self.cardSequence = [*range(len(self.fronts))]

    def flip(self):
        """flip the current card"""
        self.is_flipped = not self.is_flipped

    def get_text(self):
        """get text of current card (front or back, depending on flipped)"""
        array = self.backs if self.is_flipped else self.fronts
        if len(array) == 0:
            return ""
        else:
            currentIndex = self.cardSequence[self.current_card]
            return array[currentIndex]

    def get_number(self):
        """get current card number"""
        return self.current_card

    def next_card(self):
        """switch to next card (do nothing if already at last card)"""
        if self.current_card + 1 < len(self.fronts):
            self.current_card += 1
            self.is_flipped = False

    def prev_card(self):
        """switch to previous card (do nothing if already at first card)"""
        if self.current_card - 1 > -1:
            self.current_card -= 1
            self.is_flipped = False

    def clear_cards(self):
        self.fronts.clear()
        self.backs.clear()
        self.loaded = False

    def shuffle(self):
        random.shuffle(self.cardSequence)
        self.shuffled = True

    def unshuffle(self):
        self.cardSequence = [*range(len(self.fronts))]
        self.shuffled = False

    def toggle_shuffle(self):
        if self.shuffled:
            self.unshuffle()
        else:
            self.shuffle()

