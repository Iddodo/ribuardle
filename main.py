from audioop import reverse
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ListProperty

import kivy.metrics

from Ribuardle import Ribuardle

from kivy.core.window import Window
Window.size = (600, 600)

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
        self.lastUserInput = None
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



    

class RibuardleBoard(GridLayout, Widget):
    def __init__(self, **kwargs):
        super(RibuardleBoard, self).__init__(**kwargs)
        
        self.resize_factor = 0.5
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

        topHorizontal = []
        midHorizontal = []
        bottomHorizontal = []

        rightVertical = []
        midVertical = []
        leftVertical = []

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

    def calculateSize(self):
        #return Window.width * self.resize_factor if Window.width * self.resize_factor <= kivy.metrics.dp(500) else kivy.metrics.dp(500)
        return Window.width * self.resize_factor if Window.width * self.resize_factor <= Window.height * 0.5 - 10 else Window.height * 0.5 - 10

class RibuardleBoardContainer(Widget):
    pass

class RibuardleGame(GridLayout):
    def __init__(self, **kwargs):
        super(RibuardleGame, self).__init__(**kwargs)
        
        self.cols = 1
        self.rows = 2

        self.add_widget(RibuardleBoard())
        self.add_widget(Label(text = "Name "))


class RibuardleApp(App):
    def build(self):
        return RibuardleGame()


if __name__ == '__main__':
    RibuardleApp().run()