from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput

import kivy.metrics


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
    def __init__(self, **kwargs):
        super(LetterBox, self).__init__(**kwargs)

        self.underlyingLetter = None
        self.words = []
        self.lastUserInput = None
        self.text = None
        self.toLeft = None
        self.toRight = None
        self.toTop = None
        self.toBottom = None
        self.status = LetterStatus.UNCHECKED

    

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


        for i in range(0,25):
            self.add_widget(LetterBox())

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