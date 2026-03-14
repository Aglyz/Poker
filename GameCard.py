from random import *
from time import *

from Card import *
from Settings import *

class GameCard:

    #______________________________________________________________ Specials Variables ______________________________________________________________#

    def __init__(self, colors= Colors, values=Values32) -> None:
        self.Colors = colors
        self.Values = values
        self.Game = self.create_game(self.Colors, self.Values)

        # display cpd = Card Per View
        self.cpd = 8

    def __str__(self) -> str:
        return  str(Card.__str__(Card(), self.Game, cardPerView=self.cpd))

    #______________________________________________________________ Specials Functions ______________________________________________________________#

    #--------------------------------------------------------------- Helper Functions ---------------------------------------------------------------#

    def create_game(self, colors: tuple, values: tuple) -> list:
        return [Card(c, v) for c in colors for v in values]
    
    def shuffling(self) -> None:
        return shuffle(self.Game)

    def drawing(self, where='top') -> object:
        if where == 'top':
            return self.Game.pop(0)
        elif where == 'bottom':
            return self.Game.pop(len(self.Game)-1)
        elif where == 'random':
            return self.Game.pop(randint(0, len(self.Game))-1)
        else:
            return self.Game.pop(int(where))

    def create_hand(self, ncard=2, where='top') -> list: 
        return [self.drawing(where) for _ in range(ncard)]

    def get_forcecard(self, card: object) -> int:
        assert isinstance(card, Card), 'Your input is not a Card'
        
        if card.Value == None:
            return 0
        elif card.Value == 'A':
            return 14
        elif card.Value == 'K':
            return 13
        elif card.Value == 'Q':
            return 12
        elif card.Value == 'J':
            return 11
        else:
            return int(card.Value)

    def get_forceval(self, val: str) -> int:
        if val == 'A':
            return 14
        elif val == 'K':
            return 13
        elif val == 'Q':
            return 12
        elif val == 'J':
            return 11
        else:
            return int(val)

    def get_sum_force(self, Hand: object) -> int:
        s = 0
        for card in Hand:
            s =+ self.get_forcecard(card)
        return s

    def get_lowerforce(self) -> int:
        val = self.Values[0]
        if val == 'A':
            return 14
        elif val == 'K':
            return 13
        elif val == 'Q':
            return 12
        elif val == 'J':
            return 11
        else:
            return int(val)

    def get_higherforce(self) -> int:
        val = self.Values[-1]
        if val == 'A':
            return 14
        elif val == 'K':
            return 13
        elif val == 'Q':
            return 12
        elif val == 'J':
            return 11
        else:
            return int(val)

    def compare(self, card1: object, card2: object) -> (object | bool):
        assert isinstance(card1, Card) and isinstance(card2, Card), 'Your input(s) is(are) not a Card'

        a = self.get_forcecard(card1)
        b = self.get_forcecard(card2)
        if a > b:
            return card1
        elif b > a:
            return card2
        elif a == b:
            return None

    def Check(self, Hand: list, display=True) -> (tuple | str):
        Deck = Hand + self.Board
        occ = self.ValueOccurence(Deck)
        occ = self.SortOccurence(occ)
        straight = self.Straight(Deck, finder=True)
        flush = self.Flush(Deck, finder=True)

        if (flush != None and straight != None) and self.StraightFlush(flush, straight) != None:
            check = (self.StraightFlush(flush, straight), 'Straight Flush', 9) # Straight Flush
            if self.RoyaleFlush(check[0]) != None:
                check = (self.RoyaleFlush(check[0]), 'Royale Flush !', 10) # Royale Flush !
        elif len(occ) == 1 and occ[0][1] == 4:
            check = (self.ComboOcc(Deck, occ), 'Four of kind', 8) # Four of kind
        elif len(occ) == 2 and (occ[0][1] == 3 and occ[1][1] == 2):
            check = (self.ComboOcc(Deck, occ), 'Full House', 7) # Full House
        elif flush != None:
            check = (self.Flush(Deck), 'Flush', 6) # Flush
        elif straight != None:
            check = (self.Straight(Deck), 'Straight', 5) # Straight
        elif len(occ) == 1 and occ[0][1] == 3:
            check = (self.ComboOcc(Deck, occ), 'Tree of kind', 4) # Tree of kind
        elif len(occ) == 2 and (occ[0][1] == 2 and occ[1][1] == 2):
            check = (self.ComboOcc(Deck, occ), 'Double Pair', 3) # Double Pair
        elif len(occ) == 1 and occ[0][1] == 2:
            check = (self.HighPair(Deck), 'Pair', 2) # Pair
        else:
            check = (self.HighCard(Deck), 'High Card', 1) # High Card

        if display:
            if isinstance(check[0], Card):
                return f'{check[1]} :\n\n{check[0]}'
            else:
                return f'{check[1]} :\n\n{Card.__str__(self, check[0], 5)}'
        else:
            return check

    def ValueOccurence(self, Deck: list) -> list:
        assert not len(Deck) == 0, 'Your Deck is empty'

        Deck = self.sortAscending(Deck, reverse=True)
        occurence = []
        for i in range(2, 14+1):
            n = 0
            for card in Deck:
                if self.get_forcecard(card) == i:
                    n += 1
                    value = card.Value
            if n >= 2:
                occurence.append((value, n))
        return occurence

    def SortOccurence(self, occurence: list) -> list:
        sortedocc = []
        for n in range(2, 4+1):
            append = False
            occ = []
            for i in range(len(occurence)):
                if occurence[i][1] == n:
                    occ.append(occurence[i])
                    append = True
            if append:
                sortocc = []
                for l in range(2, 14+1):
                    for k in range(len(occ)):
                        if self.get_forceval(occurence[k][0]) == l:
                            sortocc.append(occurence[k])
                sortedocc += sortocc
        sortedocc.reverse()
        if len(sortedocc) == 3:
            sortedocc.pop(2)
        elif len(sortedocc) == 2:
            if sortedocc[0][1] == 4 and sortedocc[1][1] == 3:
                sortedocc.pop(1)
            elif sortedocc[0][1] == 3 and sortedocc[1][1] == 3:
                sortedocc[1][1] = 2
        return sortedocc

    def ComboOcc(self, Deck: list, occ: list) -> list:
        assert not len(Deck) == 0, 'Your Deck is empty'
        assert not len(occ) == 0, 'Your occurence list is empty'

        combo = []
        for i in range(len(occ)):
            for card in Deck:
                if card.Value == occ[i][0]:
                    combo.append(card)
        return combo

    def ColorOccurrence(self, Deck: list) -> list:
        Deck = self.sortAscending(Deck, reverse=True)
        occurence = []
        for color in self.Colors:
            n = 0
            for card in Deck:
                if card.Color == color:
                    n += 1
            if n >= 5:
                occurence.append((color, n))
        return occurence

    #----------------------------------------------------------------- Cards Combos -----------------------------------------------------------------#

    def HighCard(self, Deck: list) -> object:
        assert not len(Deck) == 0, 'Your Deck is empty'

        High = Deck[0]
        for card in Deck:
            if self.get_forcecard(card) > self.get_forcecard(High):
                High = card
        return High

    def LowCard(self, Deck: list) -> object:
        assert not len(Deck) == 0, 'Your Deck is empty'

        Low = Deck[0]
        for card in Deck:
            if self.get_forcecard(card) < self.get_forcecard(Low):
                Low = card
        return Low

    def HighPair(self, Deck: list) -> list:
        assert not len(Deck) == 0, 'Your Deck is empty'

        Deck = self.sortAscending(Deck, reverse=True)

        for i in range(len(Deck)-1):
            for j in range(i+1, len(Deck)):
                if Deck[i].Value is Deck[j].Value:
                    return [Deck[i], Deck[j]]

    def Straight(self, Deck: list, finder=False) -> list:
        assert not len(Deck) == 0, 'Your Deck is empty'
        assert len(Deck) >= 5, 'Your Deck must have 5 cards'

        Check = []

        for card in Deck:
            canappend = True
            for occ in Check:
                if card.Value == occ.Value:
                    canappend = False
            if canappend:
                Check.append(card)

        Check = self.sortAscending(Check, reverse=True)
        AllStraight = []

        if len(Check) < 5:
            return None

        for i in range(len(Check)):
            Straight = []
            Straight.append(Check[i])

            for j in range(1, 4+1):
                
                try:
                    if self.get_forcecard(Check[i+j]) == self.get_forcecard(Check[i])-j:
                        Straight.append(Check[i+j])
                except IndexError:
                    if self.get_forcecard(Check[(i+j)-len(Check)]) == self.get_forcecard(Check[i])+(self.get_higherforce() - self.get_lowerforce())-j+1:
                        Straight.append(Check[i+j-len(Check)])

            if len(Straight) == 5:
                for card in Straight:
                    if card not in self.Board:
                        if finder == False:
                            return Straight
                        AllStraight.append(Straight)
        if finder:
            if AllStraight == []:
                return None
            return AllStraight
        return None

    def Flush(self, Deck: list, finder=False) -> list:
        assert not len(Deck) == 0, 'Your Deck is empty'

        flush = self.ColorOccurrence(Deck)

        if flush == []:
            return None

        combo = []
        for i in range(len(flush)):
            for card in Deck:
                if card.Color == flush[i][0]:
                    combo.append(card)

        combo = self.sortAscending(combo)
        if finder:
            return combo

        if len(combo) == 5:
            for card in combo:
                if card not in self.Board:
                    return combo
        else:
            while len(combo) != 5:
                canremove = True
                for card in combo:
                    if card in self.Board and canremove == True:
                        combo.remove(card)
                        canremove = False
            return combo
        
    def StraightFlush(self, flush: list, straight: list) -> (list | None):
        assert flush is not None, "flush can't be a NoneType"
        assert straight is not None, "straight can't be a NoneType"

        for i in range(len(straight)):
            straightflush = []
            for card in straight[i]:
                if card not in flush:
                    break
                straightflush.append(card)
            if len(straightflush) == 5:
                return straightflush
        return None

    def RoyaleFlush(self, Deck: list) -> (list | None):
        assert len(Deck) == 5, 'Your Deck should be an StraightFlush'

        Deck = self.sortAscending(Deck, reverse=True)

        if Deck[0].Value == 'A' and Deck[1].Value == 'K' and Deck[2].Value == 'Q' and Deck[3].Value == 'J' and Deck[4].Value == '10':
            return Deck
        return None