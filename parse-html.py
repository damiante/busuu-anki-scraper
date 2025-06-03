#!/usr/bin/python3

from html.parser import HTMLParser


INPUT_FILE = "./vocab-page.html"
OUTPUT_FILE = "./cards.txt" # Anki likes plaintext even if the format is csv

CURRENT_CARD = None
CARDS = []


class Card():
    def __init__(self):
        self.jp_vocab = ""
        self.en_vocab = ""
        self.jp_example = ""
        self.en_example = ""

    def __repr__(self):
        return f"<Card: {jp_vocab} / {en_vocab}>"

    def export(self):
        if self.jp_example and self.en_example:
            s = self.jp_vocab + "<br>" + self.jp_example + "," + self.en_vocab + "<br>" + self.en_example + "\n"
        else:
            s = self.jp_vocab + "," + self.en_vocab + "\n"
        
        return s


class VocabPageParser(HTMLParser):


    def handle_starttag(self, tag, attrs):
        global CARDS
        global CURRENT_CARD


        if tag == "div" and attrs:
            for key, val in attrs:
                if key == "class":
                    #There are 4 unique tags used for identifying vocab pieces:
                    #Japanese vocab:   'vocab-list-row__course-language'
                    if val == "vocab-list-row__course-language":
                    # All cards have JP vocab and EN vocab; when you see JP vocab,
                    # it signals the start of a new card, so export the current one
                    # to the "done" cards and create a new one
                        if CURRENT_CARD:
                            CARDS.append(CURRENT_CARD)
                        CURRENT_CARD = Card()

                        self._next_is_jp_vocab = True

                    #Japanese example: 'vocab-list-row__keyphrase-course'
                    elif val == "vocab-list-row__keyphrase-course":
                        self._next_is_jp_example = True

                    #English vocab:    'vocab-list-row__interface-language'
                    elif val == "vocab-list-row__interface-language":
                        self._next_is_en_vocab = True

                    #English example:  'vocab-list-row__keyphrase-interface'
                    elif val == "vocab-list-row__keyphrase-interface":
                        self._next_is_en_example = True
    


    def handle_data(self, data):
        global CURRENT_CARD
        try:
            if self._next_is_jp_vocab:
                CURRENT_CARD.jp_vocab = data
                self._next_is_jp_vocab = False

            elif self._next_is_en_vocab:
                CURRENT_CARD.en_vocab = data
                self._next_is_en_vocab = False
            
            elif self._next_is_jp_example:
                CURRENT_CARD.jp_example = data
                self._next_is_jp_example = False
            
            elif self._next_is_en_example:
                CURRENT_CARD.en_example = data
                self._next_is_en_example = False
        except AttributeError:
            return


def main():

    p = VocabPageParser()

    with open(INPUT_FILE, "r") as in_f:
        for line in in_f:
            p.feed(line)

    with open(OUTPUT_FILE, "w") as out_f:
        for card in CARDS:
            out_f.write(card.export())


if __name__ == "__main__":
    main()