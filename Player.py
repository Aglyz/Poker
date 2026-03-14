from Card import *
from Settings import *

class Player:

    #______________________________________________________________ Specials Variables ______________________________________________________________#

    def __init__(self, name='Player', deck=None) -> None:
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

    def __str__(self) -> str:
        return f'\nHand of the {self.Name}:\n\n{Card.__str__(self, self.Deck)}Bank : {self.Bank}\n\n'

    #______________________________________________________________ Specials Functions ______________________________________________________________#

    def choice(self) -> str:
        print('Check: 1, Call: 2, Raise: 3, Fold: 4')
        print(Spare)
        while True:
            c = None
            try:
                c = int(input('Make your descision: '))
                print(Spare)
            except ValueError:
                print(f'Your input {c} is not a number')
                continue
            if 1 <= c and c <= 4:
                if c == 1:
                    if self.CanCheck:
                        self.State = 'Check'
                    else:
                        print('You can\'t check')
                        continue
                elif c == 2:
                    if self.CanCall:
                        self.State = 'Call'
                    else:
                        print('You can\'t call')
                        continue
                elif c == 3:
                    self.State = 'Raise'
                elif c == 4:
                    self.State = 'Fold'

                return self.State
            else:
                print('Your number must be bettween 1 and 4')

    def raising(self) -> int:
        print(Spare)
        while True:
            r = None
            try:
                r = int(input(f'How many would you raise ?\nBank : {self.Bank}\n'))
                print(Spare)
            except ValueError:
                print(f'Your input {r} is not a number')
                continue

            if r <= self.Bank:
                return r
            else:
                print(f'Your number must be bettween 1 and {self.Bank}')