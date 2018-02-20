'''
A python implementation of Pressman Toy's board game Decipher.
https://boardgamegeek.com/boardgame/189538/decipher

Number of players: 2

Description: Each player creates a 5 letter word with no repeating characters
using the letters A through Z. Remaining letters are organized alphabetically
and numbered 1 through 20 (X and Y count as a single letter.) Players alternate
turns asking for the letter on a specific number, using the results to deduce
their opponent's word.

Set Up: Create a 5 letter word and organize the remaining letters
alphabetically. Number the remaining letters 1 through 20 with X and Y counting
as a single letter.

Turn Order: On their turn, players may perform one of two actions:
    1) Pick a number between 1 and 20. The opponent will provide the
       corresponding letter for that number.

    2) Guess their opponent's five letter word.

Win Condition: Player successfully guess their opponent's 5 letter word.
'''


import string


class Player(object):
    def __init__(self, name):
        self.name = name
        self.word = ''
        self.remaining = {}
        self.received = {}

    def SetWord(self):
        validWord = False
        while not validWord:
            word = input(
                'Please provide a 5 letter word. Letters cannot be repeated. ')

            if not word.isalpha():
                print('Must use letters only.')
            elif len(word) != 5:
                print('Word must be exactly 5 letters.')
            else:
                validWord = True

                count = {}
                for letter in word:
                    if letter in count:
                        count[letter] += 1
                    else:
                        count[letter] = 1

                for letter in count:
                    if count[letter] > 1:
                        validWord = False
                        print('Cannot repeat letters: ' + letter)

        self.word = word.upper()
        print('Your word is ' + self.word)

    def SetRemaining(self):
        temp = list(string.ascii_uppercase)

        for letter in self.word:
            temp.remove(letter)

        if 'X' in self.word:
            temp.remove('Y')
        elif 'Y' in self.word:
            temp.remove('X')
        else:
            temp[temp.index('X')] = 'XY'
            temp.remove('Y')

        self.remaining = {}
        for i in range(0, 20):
            self.remaining[i + 1] = temp[i]

    def SetReceived(self):
        self.received = {}
        for i in range(0, 20):
            self.received[i + 1] = '_'

    def PrintBoard(self):
        print('These are your remaining letters:')
        for i in range(1, 6):
            print(str(i) + ' : ' + self.remaining[i] + ' | ', end='')
        print()
        for i in range(6, 11):
            if i == 10:
                print(str(i) + ': ' + self.remaining[i] + ' | ', end='')
            else:
                print(str(i) + ' : ' + self.remaining[i] + ' | ', end='')
        print()
        for i in range(11, 16):
            print(str(i) + ': ' + self.remaining[i] + ' | ', end='')
        print()
        for i in range(16, 21):
            if self.remaining[i] == 'XY':
                print(str(i) + ': ' + self.remaining[i] + '| ', end='')
            else:
                print(str(i) + ': ' + self.remaining[i] + ' | ', end='')
        print()

        print('These are your received letters: ')
        for i in range(1, 6):
            print(str(i) + ' : ' + self.received[i] + ' | ', end='')
        print()
        for i in range(6, 11):
            if i == 10:
                print(str(i) + ': ' + self.received[i] + ' | ', end='')
            else:
                print(str(i) + ' : ' + self.received[i] + ' | ', end='')
        print()
        for i in range(11, 16):
            print(str(i) + ': ' + self.received[i] + ' | ', end='')
        print()
        for i in range(16, 21):
            if self.received[i] == 'XY':
                print(str(i) + ': ' + self.received[i] + '| ', end='')
            else:
                print(str(i) + ': ' + self.received[i] + ' | ', end='')
        print()

    def WordsGuessed(self):
        pass


def GetLetter(player, opponent, move):
    num = move

    validMove = False
    while not validMove:
        if opponent.remaining[num] != '_':
            player.received[num] = opponent.remaining[num]
            opponent.remaining[num] = '_'
            validMove = True
        else:
            num = input('Already got letter. Pick another number: ')


def GuessWord(opponent, guess):
    if guess.upper() == opponent.word:
        print('Correct!')
        return True
    else:
        print('Nope.')
        return False


def Turn(player, opponent):
    while True:
        move = input('Input a number or a guess. ')

        if move.isnumeric():
            move = int(move)
            if move >= 1 and move <= 20:
                GetLetter(player, opponent, move)
                return False
        elif move.isalpha() and len(move) == 5:
            return GuessWord(opponent, move)

        print('Invalid input.')


def PlayGame(p1, p2):
    p1.SetWord()
    p1.SetRemaining()
    p1.SetReceived()

    p2.SetWord()
    p2.SetRemaining()
    p2.SetReceived()

    gameOver = False
    while not gameOver:
        print(p1.name + ' turn.')
        p1.PrintBoard()
        gameOver = Turn(p1, p2)

        if gameOver:
            print(p1.name + ' wins!')
        else:
            print(p2.name + ' turn.')
            p2.PrintBoard()
            gameOver = Turn(p2, p1)

            if gameOver:
                print(p2.name + ' wins!')


# Setup game
name1 = input('Player 1 name: ')
p1 = Player(name1)

name2 = input('Player 2 name: ')
p2 = Player(name2)

PlayGame(p1, p2)
