import WordTrie

from Enums import LetterStatus

class RibuardleSolution:
    def __init__(self, trie):
        self.trie = trie
        top_horizontal_first = WordTrie.randomHebrewLetter()
        self.topHorizontal = self.trie.randomFirstLetterWord(top_horizontal_first)
        
        right_vertical_first = self.topHorizontal.firstLetter()
        mid_vertical_first = self.topHorizontal.middleLetter()
        left_vertical_first = self.topHorizontal.lastLetter()

        self.rightVertical = self.trie.randomFirstLetterWord(right_vertical_first)
        self.midVertical = self.trie.randomFirstLetterWord(mid_vertical_first)
        self.leftVertical = self.trie.randomFirstLetterWord(left_vertical_first)

        mid_horizontal = {
            'first': self.rightVertical.middleLetter(),
            'middle': self.midVertical.middleLetter(),
            'last': self.leftVertical.middleLetter()
        }

        bottom_horizontal = {
            'first': self.rightVertical.lastLetter(),
            'middle': self.midVertical.lastLetter(),
            'last': self.leftVertical.lastLetter()
        }

        self.midHorizontal = self.trie.randomWord(mid_horizontal['first'], mid_horizontal['middle'], mid_horizontal['last'])
        self.bottomHorizontal = self.trie.randomWord(bottom_horizontal['first'], bottom_horizontal['middle'], bottom_horizontal['last'])

        self.words = [self.topHorizontal, self.midHorizontal, self.bottomHorizontal, self.rightVertical, self.midVertical, self.leftVertical]

        self.wordMatrix = [
            self.topHorizontal.label(),
            self.rightVertical.letter(1) + '#' + self.midVertical.letter(1) + '#' + self.leftVertical.letter(1),
            self.midHorizontal.label(),
            self.rightVertical.letter(3) + '#' + self.midVertical.letter(3) + '#' + self.leftVertical.letter(3),
            self.bottomHorizontal.label()
        ]

        self.lettersInSolution = []
        for word in self.words:
            for letter in word.label():
                if letter in word.label():
                    break
                self.lettersInSolution.append(letter)

    def containsDuplicates(self):
        return len(set(self.words)) < 6

class Ribuardle:
    def __init__(self, words):
        self.trie = WordTrie.WordTrie(words)

    def generateSolution(self):
        generated = False
        while (not generated):
            try:
                self.solution = RibuardleSolution(self.trie)
            except KeyError:
                pass
            else:
                generated = not self.solution.containsDuplicates()

    def testGuess(self, word, position):
    
        horizonalResult = [self.assessLetterStatus(word[j], position * 2, j) for j in range(0, 5)]
        verticalResult = [self.assessLetterStatus(word[j], j, position * 2) for j in range(0, 5)]
        
        return horizonalResult, verticalResult
    
    def assessLetterStatus(self, test_letter, row, col):
        # Correct letter
        if test_letter == self.solution.wordMatrix[row][col]:
            return LetterStatus.CORRECT
        
        # Exists in row
        in_row =  test_letter in self.solution.wordMatrix[row]
        
        # Exists in column
        in_column = test_letter in [self.solution.wordMatrix[i][col] for i in range(0,5)]

        if in_row and in_column:
            return LetterStatus.EXISTS_IN_ROW_AND_COLUMN

        if in_row:
            return LetterStatus.EXISTS_IN_ROW

        if in_column:
            return LetterStatus.EXISTS_IN_COLUMN

        if test_letter in self.solution.lettersInSolution:
            return LetterStatus.IN_PUZZLE
        
        return LetterStatus.NOT_IN_PUZZLE


    