from enum import Enum

class TokenType(Enum):
    # Symbols
    SPACE = "space"
    LPAREN = "("
    RPAREN = ")"
    LBRACK = "["
    RBRACK = "]"
    LCURL = "{"
    RCURL = "}"
    SEMICOLON = ";"
    NEG = "!"
    COMMA = ","
    DOT = "."
    UNDERSCORE = "_"
    TILDE = "~"
    # Escape Sequences
    TAB = "tab"
    NEWLINE = "newline"
    SLASH = "\\"
    DQ = "\""
    # Identifier
    IDENTIFIER = "identifier"
    # Comments
    SCOMMENT = "comment"
    # Keywords
    DINEIN = "dinein"
    TAKEOUT = "takeout"
    PINCH = "pinch"
    SKIM = "skim"
    BOOL = "bool"
    PASTA = "pasta"
    MAKE = "make"
    SERVE = "serve"
    TASTE = "taste"
    MIX = "mix"
    ELIF = "elif"
    FLIP = "flip"
    CASE = "case"
    DEFAULT = "default"
    BREAK = "chop"
    FOR = "for"
    WHILE = "simmer"
    KEEPMIX = "keepmix"
    PAR = "spit"
    YUM = "yum"
    BLEH = "bleh"
    DISH = "dish"
    HUNGRY = "hungry"
    RECIPE = "recipe"
    FULL = "full"
    CHEF = "chef"
    # Literals
    PINCHLITERALS = "pinchliterals"
    SKIMLITERALS = "skimliterals"
    PASTALITERALS = "pastaliterals"
    BOOLLITERALS = "boolliterals"

    # Assignment Operators
    ASS = "="
    ADDAS = "+="
    SUBAS = "-="
    MULAS = "*="
    DIVAS = "/="
    MODAS = "%="
    # Arithmetic Operators
    ADD = "+"
    SUB = "-"
    MUL = "*"
    DIV = "/"
    MOD = "%"
    # Relational Operators
    LT = "<"
    GT = ">"
    EQ = "=="
    NEQ = "!="
    LTE = "<="
    GTE = ">="
    # Logical Operators
    AND = "&&"
    OR = "??"
    NOT = "!!"


class Token:
    '''
    Represents a token (lexical unit) in the source code.

    Properties:
    • type: A string representing the token type.
    • value: An optional value associated with the token (e.g., numeric value, string value).

    Methods:
    • __repr__(): Generates a string representation of the token.
    '''

    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        '''
        Generates a string representation of the token.
        '''
        if self.value:
            return f"{self.type} | {self.value}"
        return f"{self.type}"