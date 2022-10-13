import random

from Enums import LetterStatus

hebrew_alphabet = 'אבגדהוזחטיכלמנסעפצקרשת'
hebrew_terminal = ['ם', 'ן', 'ף', 'ך', 'ץ']
hebrew_regular = ['מ', 'נ', 'פ', 'כ', 'צ']
def randomHebrewLetter():
    return hebrew_alphabet[random.randint(0,len(hebrew_alphabet) - 1)]

def hebrewLetterToRegular(letter):
    try:
        return hebrew_regular[hebrew_terminal.index(letter)]
    except Exception as e:
        return letter


class Word:
    def __init__(self, text):
        self.text = text

    def label(self):
        return self.text
    
    def firstLetter(self):
        return self.text[0]
    def middleLetter(self):
        return self.text[2]
    def lastLetter(self):
        return self.text[4]

    def letter(self, i):
        return self.text[i]

class WordTrieNode:
    def __init__(self):
        self.letters = dict()
        self.words = []
    
    def letterExists(self, letter):
        return letter in self.letters
    
    # Return newly created node
    def createLetterIfNotExists(self, letter):
        if not self.letterExists(letter):
            self.letters[letter] = WordTrieNode()
        return self.letters[letter]

    def addWord(self, word):
        new_word = word[:-1] + hebrewLetterToRegular(word[-1])
        self.words.append(Word(new_word))

    def getLetter(self, letter):
        return self.letters[letter]



class WordTrie:
    def __init__(self, words):
        self.rootNode = WordTrieNode()
        for word in words:
            firstLetter = word[0]
            midLetter = word[2]
            lastLetter = word[4]

            firstNode = self.rootNode.createLetterIfNotExists(firstLetter);
            midNode = firstNode.createLetterIfNotExists(midLetter);
            lastNode = midNode.createLetterIfNotExists(lastLetter);

            firstNode.addWord(word)
            lastNode.addWord(word)

    def randomWord(self, first_letter, mid_letter, last_letter):
        try:
            firstNode = self.rootNode.letters[first_letter]
            midNode = firstNode.letters[mid_letter]
            lastNode = midNode.letters[last_letter]
            words = lastNode.words
        except Exception as e:
            #print(f"Unexpected {e=}, {type(e)=}")
            raise
        else:
            rand_word_num = random.randint(0,len(words) - 1)
            return words[rand_word_num]


    def randomFirstLetterWord(self, first_letter):
        words = self.rootNode.letters[first_letter].words
        return words[random.randint(0, len(words) - 1)]

class RibuardleSolution:
    def __init__(self, trie):
        self.trie = trie
        top_horizontal_first = randomHebrewLetter()
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
        self.trie = WordTrie(words)

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


    