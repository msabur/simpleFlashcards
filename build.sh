#!/bin/sh

my_echo() {
	echo "***"
	echo $@
	echo "***"
}

APP=simple-flashcards

my_echo "Running pyinstaller"
pyinstaller simple-flashcards.spec

my_echo "Deleting unnecessary build folder"
rm -r build

my_echo "Done building! The result is in the dist folder"
