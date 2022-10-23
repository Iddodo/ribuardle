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