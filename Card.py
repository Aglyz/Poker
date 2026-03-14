class Card:

    def __init__(self, color=None, value=None) -> None:
        self.Color = color
        self.Value = value

    def __str__(self, gamecard=None, cardPerView=5, up='', mid='', down='') -> str:
        char = ''
        if isinstance(gamecard, list):
            for i in range(1, len(gamecard)+1):
                assert isinstance(gamecard[i-1], Card), 'There is something that is not a card in your game'

                card = gamecard[i-1].str_card()
                up += card[0] + '  '
                mid += card[1] + '  '
                down += card[2] + '  '

                if i%cardPerView == 0:
                    up += '\n'
                    mid += '\n'
                    down += '\n\n'
                    char += up + mid + down
                    up = ''
                    mid = ''
                    down = ''
                elif i == len(gamecard):
                    up += '\n'
                    mid += '\n'
                    down += '\n\n'
                    char += up + mid + down
        else:
            card = self.str_card()
            char += card[0] + '\n'
            char += card[1] + '\n'
            char += card[2] + '\n\n'
        return char

    def str_card(self) -> tuple:
        # Up value
        if len(self.Value) == 1:
            up = '|' + self.Value + '   ' + self.Value + '|'
        elif len(self.Value) == 2:
            up = '|' + self.Value + ' ' + self.Value + '|'

        # Symbole de Couleur
        if self.Color == 'Pique':
            mid = '|  ♠  |'
        elif self.Color == 'Trèfle':
            mid = '|  ♣  |'
        elif self.Color == 'Coeur':
            mid = '|  ♥  |'
        elif self.Color == 'Carreau':
            mid = '|  ♦  |'
        
        # Down value
        if len(self.Value) == 1:
            down = '|' + self.Value + '   ' + self.Value + '|'
        elif len(self.Value) == 2:
            down = '|' + self.Value + ' ' + self.Value + '|'
            
        return (up, mid, down)