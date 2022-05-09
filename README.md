# Simple Flashcards

A simple flashcard viewer. Make a deck of flashcards, and open it in the viewer. See the sample_decks directory for example decks.

![screenshot](./screenshots/main.png)

# Features

- Shuffle flashcards
- Supports double-sided flashcards
- Easy-to-use file format

# Usage

You can use a prebuilt binary, build your own binary, or run from source.

## Prebuilt binary (Ubuntu Linux)

1. Download the latest release
2. Extract to some location (for example, /opt)
3. Run the executable (for example, /opt/simple-flashcards/simple-flashcards)
4. Optionally, make a shortcut on the menu or desktop

## Build your own binary (Ubuntu Linux)

1. Install pyinstaller: `pip install pyinstaller`
2. Run `./build.sh`

## Running from source

1. [Install GTK dependencies](https://pygobject.readthedocs.io/en/latest/getting_started.html)
2. Optionally, start a virtualenv: `python3 -m virtualenv venv; source venv/bin/activate`
3. Run `pip install -r requirements.txt`
4. Run `python3 simple-flashcards.py`

# Format of a flashcard deck file

1. Cards are separated by a single empty line
2. A line with three dashes (---) separates the front and back of a card

