from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
Window.size = (600, 600)

class LetterBox(Widget):
    # רשימה מקושרת (למי מצביע ולאיזה כיוון)
    # לאיזה מילה / מילים שייך
    # סטטוס להראות למשתמש
    pass

class RibuardleGame(Widget):
    pass


class RibuardleApp(App):
    def build(self):
        return RibuardleGame()


if __name__ == '__main__':
    RibuardleApp().run()