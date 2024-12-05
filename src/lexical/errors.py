class Error:
    '''
    Represents an error that occurred during tokenization.

    Properties:
    • pos_start: The position where the error starts (a Position object).
    • pos_end: The position where the error ends (a Position object).
    • error_name: A string representing the type of error (e.g., "Illegal Character").
    • details: A string providing details about the error.

    Methods:
    • as_string(): Generates a formatted error message as a string.
    '''

    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        '''
        Generates a formatted error message as a string.
        '''
        result = f"{self.error_name}: {self.details}\n"
        result += f"File {self.pos_start.fn}, line {self.pos_start.ln + 1}"
        return result


class IllegalCharError(Error):
    '''
    Inherits from Error. Represents an error specifically for illegal characters.

    Properties:
    • Inherits properties from the Error class.

    Constructor:
    • __init__(pos_start, pos_end, details): Initializes an IllegalCharError object.

    Inherits the as_string() method from the Error class.
    '''

    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, "Lexical error: Illegal character/s", details)


class UnterminatedStringError(Error):
    '''
    Represents an error for unterminated strings (e.g., missing closing quote).

    Properties:
    • Inherits properties from the Error class.

    Constructor:
    • __init__(pos_start, pos_end, details): Initializes an UnterminatedStringError object.

    Inherits the as_string() method from the Error class.
    '''

    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, "Lexical error: Unterminated string error", details)


class UnterminatedCommentError(Error):
    '''
    Represents an error for unterminated comments (e.g., missing closing delimiter).

    Properties:
    • Inherits properties from the Error class.

    Constructor:
    • __init__(pos_start, pos_end, details): Initializes an UnterminatedCommentError object.

    Inherits the as_string() method from the Error class.
    '''

    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, "Lexical error: Unterminated comment error", details)


class OverflowError(Error):
    '''
    Represents an error for overflow situations.

    Properties:
    • Inherits properties from the Error class.

    Constructor:
    • __init__(pos_start, pos_end, details): Initializes an OverflowError object.

    Inherits the as_string() method from the Error class.
    '''

    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, "Lexical error: Overflow error", details)


class InvalidIdentifierError(Error):
    '''
    Represents an error for invalid identifiers.

    Properties:
    • Inherits properties from the Error class.

    Constructor:
    • __init__(pos_start, pos_end, details): Initializes an InvalidIdentifierError object.

    Inherits the as_string() method from the Error class.
    '''

    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, "Lexical error: Invalid identifier error", details)