from random import *
from math import *

from Card import *

class Bot:

    #______________________________________________________________ Specials Variables ______________________________________________________________#

    def __init__(self, name='Bot', punder=random(), deck=None) -> None:
        self.Name = name
        self.Deck = deck
        self.Score = 0
        self.Bank = 1000
        self.Blind = None
        self.State = None
        self.Bet = 0
        self.All_in = False
        self.CanCheck = True
        self.CanCall = True

        self.iter = 16

        # self.Bluff = bluff                  # Honest    0%------100%    Liar
        self.Punder = punder*2                # Thrifty   0%------100%    Spendthrifty
        # self.Carefulness = carefulness      # Naive     0%------100%    Careful

    def __str__(self) -> str:
        return f'\nHand of the {self.Name}:\n\n{Card.__str__(self, self.Deck)}Bank : {self.Bank}\n\n'

    #______________________________________________________________ Specials Functions ______________________________________________________________#

    def choice(self) -> str:
        issues = {'Check': 0, 'Call': 0, 'Raise': 0, 'Fold': 0}

        for i in range(self.iter):
            r = random()
            if 0 <= r and r < 1/6:
                issues['Fold'] += 1
            elif 1/6 <= r and r < 3/6 and self.CanCheck:
                issues['Check'] += 1
            elif 3/6 <= r and r < 5/6 and self.CanCall:
                issues['Call'] += 1
            elif 5/6 <= r and r <= 1:
                issues['Raise'] += 1

        all_m = []
        for ch in issues:
            issues[ch] = (issues[ch]/self.iter)*100
            all_m.append(issues[ch])
        m = max(all_m)
        # print(issues)

        if isclose(m, issues['Check']):
            state = 'Check'
        elif isclose(m, issues['Call']):
            state = 'Call'
        elif isclose(m, issues['Raise']):
            state = 'Raise'
        elif isclose(m, issues['Fold']):
            state = 'Fold'

        self.State = state
        return state

    def raising(self) -> int:
        r = randint(0, self.Bank)/self.Bank
        if 0 <= r and r <= self.Punder/2:
            r = randint(0, self.Bank//10)
        elif self.Punder/2 < r and r < self.Punder:
            r = randint(0, self.Bank)
        elif (self.Punder <= r and r <= 2) and self.Punder >= 1.6:
            r = self.Bank
        else:
            r = randint(0, self.Bank//(4/3))
        return r