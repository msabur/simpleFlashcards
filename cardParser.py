"""Rules
1. Put an empty line between cards
2. Put three dashes between the front and back of a card
3. Don't use these anywhere else, or the parser can get confused
"""

"""Sample file:
This is the front
---
This is the back

This is the second card
---
This is the back of the second card

What do you call the person who gives the speech of Friday prayer?
---
The khateeb!
"""

sideSeparator = '\n---\n'
cardSeparator = '\n\n'

def from_string(string):
    fronts = []; backs = []
    reading_front = True
    buffer = ''

    # removing newlines and other whitespace from the ends
    string = string.strip()

    cards = string.split('\n\n')
    for card in cards:
        sides = card.split('\n---\n')
        if len(sides) != 2:
            return None, None
        fronts.append(sides[0])
        backs.append(sides[1])

    return fronts, backs

def from_file(filename):
    with open(filename) as f:
        return from_string(f.read())
