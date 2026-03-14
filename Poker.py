from Bot import *
from GameCard import *
from Player import *

class Poker(GameCard):

    def __init__(self, colors=Colors, values=Values32) -> None:
        super().__init__(colors, values)
        self.Board = None
        
        # Players and Bots
        self.Pot = 0
        self.Blind = 10
        self.Max_amount = 0

        self.Players = [Bot(f'Bot{i}') for i in range(1, 7+1)]
        self.Players.append(Player())

    def __str__(self) -> str:
        return super().__str__()

    def __call__(self) -> None:
        return self.run()

    #______________________________________________________________ Specials Functions ______________________________________________________________#

    #--------------------------------------------------------------- Helper Functions ---------------------------------------------------------------#

    def sortAscending(self, Deck: list, reverse=False) -> list:
        assert not len(Deck) == 0, 'Your Deck is empty'

        sortedlist = []
        if reverse == True:
            for i in range(self.get_forcecard(self.HighCard(Deck))+1, self.get_forcecard(self.LowCard(Deck))-1, -1):
                for cards in Deck:
                    if self.get_forcecard(cards) == i:
                        sortedlist.append(cards)
        else:
            for i in range(self.get_forcecard(self.LowCard(Deck)), self.get_forcecard(self.HighCard(Deck))+1):
                for cards in Deck:
                    if self.get_forcecard(cards) == i:
                        sortedlist.append(cards)
        return sortedlist

    def defindBlind(self) -> None:
        assert len(self.Players) >= 2, 'Play alone is borring'

        n=0
        for i in range(len(self.Players)):
            if self.Players[i].Blind == 'BigBlind':
                try:
                    self.Players[i+1].Blind = 'BigBlind'
                except IndexError:
                    self.Players[i-len(self.Players)+1].Blind = 'BigBlind'
                self.Players[i].Blind = 'SmallBlind'
                self.Players[i-1].Blind = None
                break      
            elif self.Players[i].Blind == None:
                n+=1
        if n == len(self.Players):
            self.Players[-1].Blind = 'BigBlind'
            self.Players[-2].Blind = 'SmallBlind'

        for i in range(len(self.Players)):
            if self.Players[i].Blind == 'BigBlind':
                self.Players[i].Bank -= self.Blind
                self.Players[i].Bet += self.Blind

            if self.Players[i].Blind == 'SamllBlind':
                self.Players[i].Bank -= self.Blind//2
                self.Players[i].Bet += self.Blind//2

        self.Max_amount = self.Blind

    def Compare(self, player_1: object, player_2: object) -> (object | str):
        assert isinstance(player_1, Player) or isinstance(player_1, Bot), 'Your Player1 isn\'t a Player or Bot'
        assert isinstance(player_2, Bot) or isinstance(player_2, Player), 'Your Player2 isn\'t a Player or Bot'

        check_1 = self.Check(player_1.Deck, display=False)
        check_2 = self.Check(player_2.Deck, display=False)
        if check_1[2] > check_2[2]:
            return player_1
        elif check_2[2] > check_1[2]:
            return player_2
        elif check_1[2] == check_2[2]:
            if check_1[2] == 0 and check_2[2] == 0:
                results = GameCard.compare(self, check_1[0], check_2[0])
                if results is check_1[0]:
                    return player_1
                elif results is check_2[0]:
                    return player_2
                else:
                    return 'Equality !'
            a, b = 0, 0
            for card_1 in check_1[0]:
                a += GameCard.get_forcecard(self, card_1)
            for card_2 in check_2[0]:
                b += GameCard.get_forcecard(self, card_2)
            if a > b:
                return player_1
            elif b > a:
                return player_2
            else:
                return 'Equality !'

    def displayinfo(self) -> None:
        if len(self.Board) != 0:
            print(Card.__str__(self, self.Board))
            print(Spare)
        print(self.Players[-1])
        if len(self.Board) >= 3:
            print(self.Check(self.Players[-1].Deck, self.Board))

    #_____________________________________________________________________ Main _____________________________________________________________________#

    def reset(self) -> None:
        self.Game = GameCard(self.Colors, self.Values)

        for players in self.Players:
            players.Deck = None
            players.Bet = 0

        self.Pot = 0
        self.Max_amount = 0
        self.Board = self.Game.create_hand(0)

    def initialisation(self) -> None:
        self.reset()
        self.Game.shuffling()
        self.cpd = 14

        for players in self.Players:
            players.Deck = self.Game.create_hand(2, where='bottom')

        self.defindBlind()

    def biddingRound(self) -> None:
        
        for i in range(len(self.Players)):
            if self.Players[i].Blind == 'BigBlind':
                if i+1 > len(self.Players)-1:
                    utg = i-len(self.Players)+1
                else:
                    utg = i+1

        AllCheck = True
        OneLoop = False

        while True:
            havefold = False
            haveraise = False

            if self.Players[utg].State != 'Fold' and self.Players[utg].All_in == False:

                if self.Players[utg].Bet == self.Max_amount:
                    self.Players[utg].CanCheck = True
                    self.Players[utg].CanCall = False
                else:
                    self.Players[utg].CanCheck = False
                    self.Players[utg].CanCall = True
    

                choice = self.Players[utg].choice()

                if choice != 'Check':
                    AllCheck = False
                
                if choice == 'Call':
                    diff = self.Max_amount - self.Players[utg].Bet
                    if diff == self.Players[utg].Bank:
                        self.Players[utg].All_in = True # All-in
                    elif diff >= self.Players[utg].Bank:
                        self.Players[utg].All_in = True # All-in Partial

                    if diff < self.Players[utg].Bank:
                        self.Players[utg].Bet += diff
                        self.Players[utg].Bank -= diff
                    else:
                        self.Players[utg].Bet += self.Players[utg].Bank
                        self.Players[utg].Bank = 0

                elif choice == 'Raise':
                    r = self.Players[utg].raising()
                    if r == self.Players[utg].Bank:
                        self.Players[utg].All_in = True

                    self.Max_amount += r
                    self.Players[utg].Bet += r
                    self.Players[utg].Bank -= r
                    haveraise = True

                elif choice == 'Fold':
                    havefold = True

            char = f'{self.Players[utg].Name} have: {self.Players[utg].State}'

            if haveraise:
                char += f' of {r}.'
            if self.Players[utg].All_in == True:
                char += ' All in !'

            char += f'\n\nMax Amount: {self.Max_amount} Pot : {self.Pot}'

            if self.Players[utg].State != 'Fold' or havefold:
                print(char)
                print(Spare)
                sleep(1)
            
            if self.Players[utg].Blind == 'BigBlind':
                OneLoop = True
                if AllCheck:
                    break
            
            if OneLoop:
                Same_Amount = True
                All_All_In = True
                for i in range(len(self.Players)):
                    if self.Players[i].State != 'Fold':
                        if self.Players[i].All_in == False:
                            All_All_In = False
                            break
                if All_All_In:
                    break
                max_bet = 0
                for i in range(len(self.Players)):
                    if self.Players[i].State != 'Fold':
                        if self.Players[i].Bet > max_bet:
                            max_bet = self.Players[i].Bet
                for i in range(len(self.Players)):
                    if self.Players[i].State != 'Fold':
                        if not(self.Players[i].All_in):
                            if max_bet != self.Players[i].Bet:
                                Same_Amount = False
                                break
                        elif self.Players[i].All_in:
                            if not(self.Players[i].Bet <= max_bet):
                                Same_Amount = False
                                break
                if Same_Amount:
                    break
                
            if utg == len(self.Players)-1:
                utg = (utg-len(self.Players))+1
            else:
                utg += 1

        for i in range(len(self.Players)):
            self.Pot += self.Players[i].Bet
            self.Players[i].Bet = 0
        self.Max_amount = 0

    def win(self) -> None:
        for players in self.Players:
            if players.State != 'Fold':
                print(f'{players.Name} :\n')
                print(Card.__str__(self, players.Deck))
                print(self.Check(players.Deck))
                print(Spare)

        winner = []
        for i in range(len(self.Players)):
            if self.Players[i].State != 'Fold' and len(winner) != 0:
                win = self.Compare(self.Players[i], winner[0])

                if win is self.Players[i]:
                    winner = []
                    winner.append(self.Players[i])
                elif win == 'Equality !':
                    winner.append(self.Players[i])

            elif self.Players[i].State != 'Fold' and len(winner) == 0:
                winner.append(self.Players[i])
        
        for win in winner:
            win.Bank += self.Pot // len(winner)

        if len(winner) == 1:
            print(f'{winner[0].Name} win the game, an the pot of {self.Pot}!')
        else:
            char = ''
            for i in range(len(winner)):
                char += f'{winner[i].Name}, '
            print(f'The winners are {char} !')

    def flop(self) -> None:
        for _ in range(3):
            self.Board.append(self.Game.drawing())

    def turn(self) -> None:
        self.Board.append(self.Game.drawing())

    def river(self) -> None:
        self.Board.append(self.Game.drawing())

    #--------------------------------------------------------------------- Runs ---------------------------------------------------------------------#
    
    def run(self) -> None:
        self.initialisation()

        self.displayinfo()
        self.biddingRound()
        self.flop()
        self.displayinfo()
        self.biddingRound()
        self.turn()
        self.displayinfo()
        self.biddingRound()
        self.river()
        self.displayinfo()
        self.biddingRound()

        self.win()

    #-------------------------------------------------------------------- States --------------------------------------------------------------------#