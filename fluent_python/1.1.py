#!/usr/bin/python3

from random import shuffle


class Card:
    __slots__ = ("rank", "suit")
    # _suits_d = dict(spades='\u2660', hearts='\u2665', clubs='\u2663',
    #                 diamonds='\u2666')

    def __init__(self, rank, suit):
        self.rank = str(rank).capitalize()
        self.suit = suit

    def __eq__(self, y):
        if hash(self) == hash(y):
            return True

    def __hash__(self):
        return hash((self.rank, self.suit))

    def __repr__(self):
        return f"{chr(self.unicode())}"
        # return f'{chr(self.unicode())} {self._suits_d[self.suit]} {
        # self.rank}'

    def __unicode__(self):
        offset = 0x1F0A0
        if self == Card("White", "joker"):
            return 0x1F0DF
        elif self == Card("Red", "joker"):
            return 0x1F0BF
        else:
            pass
        _ranks_u = (
            [
                "A",
            ]
            + [str(n) for n in range(2, 11)]
            + list("JQK")
        )
        _suits_u = "spades hearts diamonds clubs".split()
        rank_u = _ranks_u.index(self.rank)
        suit_u = _suits_u.index(self.suit)
        card_u = offset + rank_u + 1 + suit_u * 16
        return card_u


class Deck:
    _ranks = (
        [str(n) for n in range(3, 11)]
        + list("JQKA")
        + [
            "2",
        ]
    )
    _suits = "diamonds clubs hearts spades".split()

    # card_n = rank_n + 1 + suit_n * 13
    def __init__(self, joker=False):
        self.raw_cards = [
            Card(rank, suit) for rank in self._ranks for suit in self._suits
        ]
        if joker:
            self.raw_cards.extend([Card("red", "joker"), Card("white", "joker")])
        self.cards = self.raw_cards[::]

    def __getitem__(self, position):
        return self.cards[position]

    def __len__(self):
        return len(self.cards)

    def __repr__(self):
        return " ".join([str(i) for i in self.cards])

    def value(self, card):
        return self.raw_cards.index(card)
        # return (self._ranks.index(card.rank) * len(self._suits) +
        #         self._suits.index(card.suit) + 1)

    def shuffle(self):
        shuffle(self.cards)


a = Deck()
print(a, len(a))
a.shuffle()
print(a)
b = Deck(joker=True)
c = Card(5, "clubs")
print(b, len(b))
print(b.value(c))
b.shuffle()
print(b)
print(b.value(c))
