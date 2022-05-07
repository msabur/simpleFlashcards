"""A deck of flashcards"""
class CardDeck:
    def __init__(self):
        self.loaded = False
        self.fronts = []
        self.backs = []
        self.current_card = 0
        self.is_flipped = False

    def load_data(self, fronts, backs):
        # Doing some input validation
        if not isinstance(fronts, list) or not isinstance(backs, list):
            raise ValueError("Invalid card data")
        elif len(fronts) != len(backs):
            raise ValueError("Invalid card data")
        else:
            self.clear_cards()
            for front, back in zip(fronts, backs):
                self.fronts.append(front)
                self.backs.append(back)
            self.loaded = True

    def loadSampleData(self):
        self.clear_cards()
        cards = ['deen', 'religion', 'kurah', 'ball', 'inab', 'grape',
                'فيل', 'elephant', 'umm', 'mother', 'ab', 'father']
        for front in cards[::2]:
            self.fronts.append(front)
        for back in cards[1::2]:
            self.backs.append(back)
        self.loaded = True

    def flip(self):
        """flip the current card"""
        self.is_flipped = not self.is_flipped

    def get_text(self):
        """get text of current card (front or back, depending on flipped)"""
        array = self.backs if self.is_flipped else self.fronts
        if len(array) == 0:
            return ""
        else:
            return array[self.current_card]

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

