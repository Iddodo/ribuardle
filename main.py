from audioop import reverse
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ListProperty

import kivy.metrics

from Ribuardle import Ribuardle

from kivy.core.window import Window
Window.size = (800, 800)

from enum import Enum

class LetterStatus(Enum):
    UNCHECKED = 1
    EXISTS_IN_ROW = 2
    EXISTS_IN_COLUMN = 3
    EXISTS_IN_ROW_AND_COLUMN = 4
    NOT_IN_PUZZLE = 5
    CHECKED = 6
    BUFFER = 7

class LetterBox(Widget):
    def __init__(self, letter = '', word = None, left = None, right = None, top = None, bottom = None, status = LetterStatus.UNCHECKED, **kwargs):
        self.underlyingLetter = letter
        self.words = [word]
        self.lastUserInput = ''
        self.toLeft = left
        self.toRight = right
        self.toTop = top
        self.toBottom = bottom
        self.rgba = ListProperty((1,1,1,1))
        self.setStatus(status)
        super(LetterBox, self).__init__(**kwargs)
        # Design LetterBox according to status
    
    def setStatus(self, status):
        if status == LetterStatus.BUFFER:
            self.rgba = (0,0,0,1)
        else:
            self.rgba = (1,1,1,1)
        
        self.status = status

    def setLetter(self, letter):
        self.lastUserInput = letter
        self.ids.label.text = letter

    def validateLetter(self):
        if self.underlyingLetter == self.lastUserInput:
            print('xD')

    

class RibuardleBoard(GridLayout, Widget):
    numTurnsInRound = 3
    turn = 0
    turnWordIndex = 0
    remainingTurns = 10
    
    topHorizontal = []
    midHorizontal = []
    bottomHorizontal = []

    rightVertical = []
    midVertical = []
    leftVertical = []

    lettersIn = {
        topHorizontal: [],
    }

    turnMapping = {
            0: [topHorizontal, rightVertical],
            1: [midHorizontal, midVertical],
            2: [bottomHorizontal, leftVertical]
    }
    def letterBoxListToWord(self, lst):
        return [box.underlyingLetter() for box in lst].join('')
    def calculateSize(self):
        return Window.width * self.resize_factor if Window.width * self.resize_factor <= kivy.metrics.dp(500) else kivy.metrics.dp(500)
        #return Window.width * self.resize_factor if Window.width * self.resize_factor <= (Window.height * 0.8 - 10) else (Window.height * 0.8 - 10)
        #return 700
    def __init__(self, **kwargs):
        super(RibuardleBoard, self).__init__(**kwargs)
        
        self.resize_factor = 0.8
        self.cols = 5
        self.rows = 5
        self.spacing = (10, 10)
        self.padding = (10, 10)
        self.width = self.calculateSize()
        self.height = self.calculateSize()
        with open('hebrew-five-letter-words.txt', encoding='utf-8') as file:
            words = file.readlines()
            rib = Ribuardle(words)
            rib.generateSolution()

        self.solution = rib

        topHorizontal = self.topHorizontal
        midHorizontal = self.midHorizontal
        bottomHorizontal = self.bottomHorizontal

        rightVertical = self.rightVertical
        midVertical = self.midVertical
        leftVertical = self.leftVertical

        buffer_boxes = [LetterBox(status = LetterStatus.BUFFER) for i in range(0,4)]

        topHorizontal.append(LetterBox(letter = rib.solution.topHorizontal.firstLetter(), word = rib.solution.topHorizontal))
        topHorizontal[0].words.append(rib.solution.rightVertical)

        for i in range(1,5):
            topHorizontal.append(LetterBox(letter = rib.solution.topHorizontal.letter(i), word = rib.solution.topHorizontal, right = topHorizontal[i - 1]))
            topHorizontal[i - 1].toLeft = topHorizontal[i]

        rightVertical.append(topHorizontal[0])
        rightVertical[0].words.append(rib.solution.rightVertical)
        for i in range(1,5):
            rightVertical.append(LetterBox(letter = rib.solution.rightVertical.letter(i), word = rib.solution.rightVertical, top = rightVertical[i - 1]))
            rightVertical[i - 1].toBottom = rightVertical[i]
        
        midHorizontal.append(rightVertical[2])
        midHorizontal[0].words.append(rib.solution.midHorizontal)

        for i in range(1, 5):
            midHorizontal.append(LetterBox(letter = rib.solution.midHorizontal.letter(i), word = rib.solution.midHorizontal, right = midHorizontal[i - 1]))
            midHorizontal[i - 1].toLeft = midHorizontal[i]

        #handle middle letters later

        leftVertical.append(topHorizontal[4])
        leftVertical[0].words.append(rib.solution.leftVertical)
        for i in range(1,5):
            leftVertical.append(LetterBox(letter = rib.solution.leftVertical.letter(i), word = rib.solution.leftVertical, top = leftVertical[i - 1]))
            leftVertical[i - 1].toBottom = leftVertical[i]
        
        
        bottomHorizontal.append(rightVertical[4])
        bottomHorizontal[0].words.append(rib.solution.bottomHorizontal)
        for i in range(1,5):
            bottomHorizontal.append(LetterBox(letter = rib.solution.bottomHorizontal.letter(i), word = rib.solution.bottomHorizontal, right = bottomHorizontal[i - 1]))
            bottomHorizontal[i - 1].toLeft = bottomHorizontal[i]
        
        midVertical.append(topHorizontal[2])
        midVertical[0].words.append(rib.solution.midVertical)
        for i in range(1,5):
            midVertical.append(LetterBox(letter = rib.solution.midVertical.letter(i), word = rib.solution.midVertical, top = midVertical[i - 1]))
            midVertical[i - 1].toBottom = midVertical[i]

        # Three points to change according to order
        #-U|R-M|L-B

        midHorizontal[2].toTop = midVertical[2].toTop
        midHorizontal[2].toBottom = midVertical[2].toBottom
        midVertical[2] = midHorizontal[2]
        midVertical[2].words.append(rib.solution.midVertical)

        midHorizontal[4].toTop = leftVertical[2].toTop
        midHorizontal[4].toBottom = leftVertical[2].toBottom
        leftVertical[2] = midHorizontal[4]
        leftVertical[2].words.append(rib.solution.leftVertical)

        leftVertical[4].toRight = bottomHorizontal[4].toRight
        bottomHorizontal[4] = leftVertical[4]
        leftVertical[4].words.append(rib.solution.leftVertical)

        bottomHorizontal[2].toTop = midVertical[4].toTop
        midVertical[4] = bottomHorizontal[2]
        midVertical[4].words.append(rib.solution.midVertical)

        # add arrays 

        boxes = list(reversed(topHorizontal)) # First row
        boxes += [leftVertical[1], buffer_boxes[0], midVertical[1], buffer_boxes[1], rightVertical[1]] # Second row
        boxes += list(reversed(midHorizontal)) # Third row
        boxes += [leftVertical[3], buffer_boxes[2], midVertical[3], buffer_boxes[3], rightVertical[3]] # Fourth row
        boxes += list(reversed(bottomHorizontal)) # Fifth row

        for box in boxes:
            self.add_widget(box)

    def on_size(self, *args):
        self.height = self.calculateSize()
        self.width = self.calculateSize()

    def incrementTurn(self):
        if self.remainingTurns <= 0:
            print("meow")
            raise
        self.turn += 1
        self.remainingTurns -= 1
        print(self.remainingTurns)
        self.turnWordIndex = 0

    def passKey(self, userLetter):
        firstWord, secondWord = self.turnMapping[self.turn % self.numTurnsInRound]
        if userLetter == 'enter':
            if self.turnWordIndex != 5:
                return
            
            self.incrementTurn()
        elif userLetter == 'backspace':
            if self.turnWordIndex <= 0:
                return
            
            self.turnWordIndex -= 1
            firstWord[self.turnWordIndex].setLetter('')
            secondWord[self.turnWordIndex].setLetter('')

        else:
            if self.turnWordIndex == 5:
                return
            
            firstWord[self.turnWordIndex].setLetter(userLetter)
            secondWord[self.turnWordIndex].setLetter(userLetter)
            self.turnWordIndex = self.turnWordIndex + 1
            


class RibuardleBoardContainer(Widget):
    pass

class RibuardleGame(GridLayout):
    hebrew_keycode = 'קראטופשדגכעיחלזסבהנמצת'
    english_keycode = 'ertyupasdfghjkzxcvbnm,'

    def englishLetterToHebrew(self, letter, keycode = -1):
        # This line is needed for Hebrew layout
        if keycode == 1514:
            return 'ת'
        
        # Allow backspace and enter keys
        elif keycode == 8:
            return 'backspace'

        elif keycode == 13:
            return 'enter'

        return self.hebrew_keycode[self.english_keycode.index(letter)]

    def getTurnWords(self):
        return self.board.getTurnWords(self.turn % self.numTurnsInRound)

    def __init__(self, **kwargs):

        self.userLetter = '?'
        self.turns = -1

        super(RibuardleGame, self).__init__(**kwargs)

        self.board = self.ids.board_container.ids.ribuardle_board

        # Listen to keyboard
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        try:
            self.userLetter = self.englishLetterToHebrew(keycode[1], keycode[0])
        except Exception as e:
            return

        self.ids.controls_label.text = self.userLetter
        print(self.userLetter + " " + str(keycode[0]))

        self.board.passKey(self.userLetter)
        #self.turns = self.board.turn


class RibuardleApp(App):
    def build(self):
        return RibuardleGame()


if __name__ == '__main__':
    RibuardleApp().run()