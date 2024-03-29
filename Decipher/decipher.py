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
    def __init__(self, number):
        self.number = number
        self.name = ''
        self.word = ''
        self.remaining = {}
        self.received = {}

    def InputName(self):
        name = input("What's your name? ")
        self.name = name

    def InputWord(self):
        word = input(
            'Please provide a 5 letter word. Letters cannot be repeated. XY is considered one letter and cannot be used at the same time. ')
        self.word = word.upper()

    def SetRemainingBoard(self):
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

        for i in range(0, 20):
            self.remaining[i + 1] = temp[i]

    def SetReceivedBoard(self):
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

    def ValidWord(self, word):
        valid = True

        # Checking for an empty string first so the 5 letter instruction doesn't get repeated unnecessarily.
        if word == '':
            valid = False
        elif 'XY' in word.upper():
            print('X and Y is considered one letter and cannot be used at the same time.')
            valid = False
        elif len(word) != 5:
            print('Word must be exactly 5 letters.')
            valid = False
        elif not word.isalpha():
            print('Must use letters only.')
            valid = False
        else:
            count = {}
            for letter in word:
                count[letter] = count.get(letter, 0) + 1

            # Using two loops displays multiple repeated letters in a cleaner format.
            for letter in count:
                if count[letter] > 1:
                    print('Cannot repeat letters: ' + letter.upper())
                    valid = False

        return valid

    def WordsGuessed(self):
        pass


class Computer(Player):
    def __init__(self):
        # Set up iniital guessing board.
        self.lookup = list(string.ascii_uppercase)
        self.lookup[23] = 'XY'
        self.lookup.remove('Y')
        self.potential = self.lookup.copy()
        self.deduction = {}

        for i, letter in enumerate(self.lookup):
            if i < 20:
                self.deduction[i + 1] = {'Min': letter,
                                         'Max': self.lookup[i + 5], 'Known': False}

    def SetKnown(self, num):
        if self.deduction[num]['Min'] == self.deduction[num]['Max']:
            self.deduction[num]['Known'] = True
            self.potential.remove(self.deduction[num]['Min'])

    def SetReceivedLetter(self, num, received):
        self.deduction[num] = {'Min': received, 'Max': received, 'Known': True}
        self.potential.remove(received)

    def UpdateMax(self, num):
        if not self.deduction[num]['Known'] and num != 20:
            nextMaxLetter = self.deduction[num + 1]['Max']
            maxIndex = self.lookup.index(nextMaxLetter) - 1
            self.deduction[num]['Max'] = self.lookup[maxIndex]

            self.SetKnown(num)

    def UpdateMin(self, num):
        if not self.deduction[num]['Known']:
            prevMinLetter = self.deduction[num - 1]['Min']
            minIndex = self.lookup.index(prevMinLetter) + 1
            self.deduction[num]['Min'] = self.lookup[minIndex]

            self.SetKnown(num)


def GetLetter(player, opponent, move):
    player.received[move] = opponent.remaining[move]
    opponent.remaining[move] = '_'
    print('Received {}: {}'.format(move, player.received[move]))


def GuessWord(opponent, guess):
    if guess.upper() == opponent.word:
        print('Correct!')
        return True
    else:
        print("Incorrect. {} is not {}'s word.".format(guess, opponent.name))
        return False


def InputMove():
    return input('Input a number between 1 and 20 or a 5 letter guess. ')


def LeaveGame():
    quit()


def Turn(player, opponent):
    while True:
        move = InputMove()

        if not ValidMove(player, opponent, move):
            print('Invalid move.')
        else:
            break

    if move.isnumeric():
        GetLetter(player, opponent, int(move))
        return False
    else:
        return GuessWord(opponent, move)


def ValidMove(player, opponent, move):
    if move == "exit()" or move == "quit()":
        return LeaveGame()
    elif move.isnumeric():
        move = int(move)
        if move >= 1 and move <= 20:
            if player.received[move] == '_' and opponent.remaining[move] != '_':
                return True
            elif player.received[move] != '_' and opponent.remaining[move] == '_':
                print('Already have that letter. Choose another number.')
                return False
        else:
            return False
    elif move.isalpha() and len(move) == 5:
        return True
    else:
        return False


def PlayGame():
    print('PLAYER 1')
    p1 = Player(1)
    p1.InputName()

    while not p1.ValidWord(p1.word):
        p1.InputWord()
    print('Your word is ' + p1.word)

    p1.SetRemainingBoard()
    p1.SetReceivedBoard()

    print('PLAYER 2')
    p2 = Player(2)
    p2.InputName()

    while not p2.ValidWord(p2.word):
        p2.InputWord()
    print('Your word is ' + p2.word)

    p2.SetRemainingBoard()
    p2.SetReceivedBoard()

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


if __name__ == '__main__':
    PlayGame()
