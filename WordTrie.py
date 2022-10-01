import random

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
            print(f"Unexpected {e=}, {type(e)=}")
            raise
        else:
            rand_word_num = random.randint(0,len(words) - 1)
            return words[rand_word_num]


    def randomFirstLetterWord(self, first_letter):
        words = self.rootNode.letters[first_letter].words
        return words[random.randint(0, len(words) - 1)]

class RibuardleBoard:
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

    def containsDuplicates(self):
        return len(set(self.words)) < 6

class Ribuardle:
    def __init__(self, words):
        self.trie = WordTrie(words)

    def generateBoard(self):
        generated = False
        while (not generated):
            try:
                self.board = RibuardleBoard(self.trie)
            except KeyError:
                pass
            else:
                generated = not self.board.containsDuplicates()

with open('hebrew-five-letter-words.txt') as file:
    words = file.readlines()
    rib = Ribuardle(words)
    rib.generateBoard()


    print(rib.board.topHorizontal.label()[::-1])
    print(rib.board.midHorizontal.label()[::-1])
    print(rib.board.bottomHorizontal.label()[::-1])

    print(rib.board.rightVertical.label()[::-1])
    print(rib.board.midVertical.label()[::-1])
    print(rib.board.leftVertical.label()[::-1])


    