#Copyright (c) 2009,10 Walter Bender

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

import pygtk
pygtk.require('2.0')
import gtk
from random import randrange

from constants import HIGH, FILLS, SHAPES, NUMBER, COLORS
from card import Card
from gencards import generate_pattern_card, generate_number_card, \
                     generate_word_card


class Deck:
    """ Class for defining deck of card """

    def __init__(self, sprites, card_type, numbers_type, word_lists, scale,
                 level=HIGH):
        """ Create the deck of cards. """
        self.cards = []
        # If level is 'simple', only generate one fill type
        if level == HIGH:
            fill_range = FILLS
        else:
            fill_range = 1
        # Initialize the deck of cards by looping through all the patterns
        for shape in range(0, SHAPES):
            for color in range(0, COLORS):
                for num in range(0, NUMBER):
                    for fill in range(0, fill_range):
                        if card_type == 'pattern':
                            self.cards.append(Card(sprites,
                                                   generate_pattern_card(shape,
                                                   color, num, fill, scale),
                                                   [shape, color, num, fill]))
                        elif card_type == 'number':
                            self.cards.append(Card(sprites,
                                                   generate_number_card(shape,
                                                       color, num, fill,
                                                       numbers_type, scale),
                                                   [shape, color, num, fill]))
                        else:
                            self.cards.append(Card(sprites,
                                                   generate_word_card(shape,
                                                   color, num, fill, scale),
                                                   [shape, color, num, fill]))
                            self.cards[len(self.cards) - 1].spr.set_label(
                                                   word_lists[shape][num])
                            self.cards[len(self.cards)\
                                      - 1].spr.set_label_color(
                                                   COLOR_PAIRS[color][0])
                            self.cards[len(self.cards)\
                                      - 1].spr.set_label_attributes(scale * 24)
                            if fill == 0:
                                self.cards[len(self.cards)\
                                      - 1].spr.set_font('Sans Bold')
                            elif fill == 2:
                                self.cards[len(self.cards)\
                                      - 1].spr.set_font('Sans Italic')

        # Remember the current position in the deck.
        self.index = 0

    def shuffle(self):
        """ Shuffle the deck (Knuth algorithm). """
        decksize = self.count()
        # Hide all the cards.
        for c in self.cards:
            c.hide_card()
        # Randomize the card order.
        for n in range(decksize):
            i = randrange(decksize - n)
            self.swap_cards(n, decksize - 1 - i)
        # Reset the index to the beginning of the deck after a shuffle,
        self.index = 0
        return

    def restore(self, saved_deck_indices):
        """ Restore the deck upon resume. """
        decksize = len(saved_deck_indices)
        # If we have a short deck, then we need to abort.
        if self.count() < decksize:
            return False
        _deck = []
        for i in saved_deck_indices:
            _deck.append(self.index_to_card(i))
        for i in range(decksize):
            self.cards[i] = _deck[i]
        return True

    def swap_cards(self, i, j):
        """ Swap the position of two cards in the deck. """
        tmp = self.cards[j]
        self.cards[j] = self.cards[i]
        self.cards[i] = tmp
        return

    def spr_to_card(self, spr):
        """ Given a sprite, find the corresponding card in the deck. """
        for c in self.cards:
            if c.spr == spr:
                return c
        return None

    def index_to_card(self, i):
        """ Given a card index, find the corresponding card in the deck. """
        for c in self.cards:
            if c.index == i:
                return c
        return None

    def deal_next_card(self):
        """ Return the next card from the deck. """
        if self.empty():
            return None
        next_card = self.cards[self.index]
        self.index += 1
        return next_card

    def empty(self):
        """ Is the deck empty? """
        if self.cards_remaining() > 0:
            return False
        else:
            return True

    def cards_remaining(self):
        """ Return how many cards are remaining in the deck. """
        return(self.count() - self.index)

    def hide(self):
        """ Hide the deck. """
        for c in self.cards:
            if c is not None:
                c.hide_card()

    def count(self):
        """ Return the length of the deck. """
        return len(self.cards)
