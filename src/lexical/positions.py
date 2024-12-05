class Position:
    '''
    Represents a position in the source code.

    Properties:
    • idx: An integer representing the character index in the source code.
    • ln: An integer representing the line number.
    • col: An integer representing the column number.
    • fn: A string representing the source file name.
    • ftxt: A string representing the source code text.

    Methods:
    • advance(current_char): Updates the position based on the current character.
    • copy(): Creates a copy of the current Position object.
    • reset(): Resets the position to its initial state by setting the character index and column number to 0.
    '''

    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, current_char):
        '''
        Updates the position based on the current character.
        '''
        self.idx += 1
        self.col += 1

        if current_char == "\n":
            self.ln += 1
            self.col = 0

        return self

    def copy(self):
        '''
        Creates a copy of the current Position object.
        '''
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)

    def reset(self):
        '''
        Resets the position to its initial state by setting the character index and column number to 0.
        '''
        self.idx = 0
        self.col = 0