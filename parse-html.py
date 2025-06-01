#!/usr/bin/python3

from html.parser import HTMLParser


INPUT_FILE = "./vocab-page.html"
OUTPUT_FILE = "./cards.txt" # Anki likes plaintext even if the format is csv

JAPANESE_TEXT = []
ENGLISH_TEXT = []


class VocabPageParser(HTMLParser):


    def handle_starttag(self, tag, attrs):

        #case when japanese vocab piece
        if tag == "span" and attrs:
            for key, val in attrs:
                if key == "class" and val == "font-face-ja":
                    self._next_is_japanese = True

        #case when english translation
        if tag == "div" and attrs:
            for key, val in attrs:
                if key == "class" and (val == "vocab-list-row__interface-language" or val == "vocab-list-row__keyphrase-interface"):
                    self._next_is_english = True


    def handle_data(self, data):
        try:
            # Case for card front
            if self._next_is_japanese:
                global JAPANESE_TEXT
                JAPANESE_TEXT.append(data)
                self._next_is_japanese = False
            # Case for card back
            elif self._next_is_english:
                global ENGLISH_TEXT
                ENGLISH_TEXT.append(data)
                self._next_is_english = False
        except AttributeError:
            return


def main():

    p = VocabPageParser()

    with open(INPUT_FILE, "r") as in_f:
        for line in in_f:
            p.feed(line)

    global JAPANESE_TEXT
    JAPANESE_TEXT = [x for x in JAPANESE_TEXT if not x.isdigit()]

    with open(OUTPUT_FILE, "w") as out_f:
        CARD_FRONTS = JAPANESE_TEXT[::2]
        EXAMPLE_JAPANESE = JAPANESE_TEXT[1::2]
        CARD_BACKS = ENGLISH_TEXT[::2]
        EXAMPLE_ENGLISH = ENGLISH_TEXT[1::2]
        for front, example, back, translation in zip(CARD_FRONTS, EXAMPLE_JAPANESE, CARD_BACKS, EXAMPLE_ENGLISH):
            out_f.write(front + "<br>" + example + "," + back + "<br>" + translation + "\n")
    






if __name__ == "__main__":
    main()