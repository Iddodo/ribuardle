from enum import Enum

class LetterStatus(Enum):
    UNCHECKED = 1
    EXISTS_IN_ROW = 2
    EXISTS_IN_COLUMN = 3
    EXISTS_IN_ROW_AND_COLUMN = 4
    NOT_IN_PUZZLE = 5
    IN_PUZZLE = 6
    CORRECT = 7
    BUFFER = 8
    



    def getColor(e):
        return letter_status_colors[e]


letter_status_colors = {
    LetterStatus.BUFFER: (0,0,0,1),
    LetterStatus.EXISTS_IN_ROW: (1, 0, 0, 1),
    LetterStatus.EXISTS_IN_COLUMN: (1, 1, 0, 1),
    LetterStatus.EXISTS_IN_ROW_AND_COLUMN: (1, 165/255, 0, 1),
    LetterStatus.NOT_IN_PUZZLE: (0.2, 0.2, 0.2, 1),
    LetterStatus.IN_PUZZLE: (1, 1, 1, 1),
    LetterStatus.CORRECT: (0, 1, 0, 1),
    LetterStatus.UNCHECKED: (0.5, 0.5, 0.5, 1),
}