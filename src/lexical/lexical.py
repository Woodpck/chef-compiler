from rply import LexerGenerator, Token
from src.lexical.positions import Position
from src.lexical.errors import (
    IllegalCharError, 
    UnterminatedStringError, 
    InvalidIdentifierError
)

class Lexer:
    def __init__(self, fn='<stdin>'):
        self.fn = fn
        self.lexer = LexerGenerator()
        self.tokens = []
        self.errors = []

    def _add_tokens(self):
        # Keywords
        reserved_keywords = {
            'dinein': 'DINEIN',
            'takeout': 'TAKEOUT',
            'pinch': 'PINCH',
            'skim': 'SKIM',
            'bool': 'BOOL',
            'pasta': 'PASTA',
            'make': 'MAKE',
            'serve': 'SERVE',
            'taste': 'TASTE',
            'mix': 'MIX',
            'elif': 'ELIF',
            'flip': 'FLIP',
            'case': 'CASE',
            'default': 'DEFAULT',
            'chop': 'BREAK',
            'for': 'FOR',
            'simmer': 'WHILE',
            'keepmix': 'KEEPMIX',
            'spit': 'SPIT',
            'yum': 'YUM',
            'bleh': 'BLEH',
            'dish': 'DISH',
            'hungry': 'HUNGRY',
            'recipe': 'RECIPE',
            'full': 'FULL',
            'chef': 'CHEF'
        }
        for keyword, token_name in reserved_keywords.items():
            self.lexer.add(token_name, rf'\b{keyword}\b')

        # Symbols
        symbols = {
            r'\\': 'BACKSLASH',
            r'\}': 'RBRACE',
            r'\]': 'RBRACKET',
            r'&&': 'AND',
            r'\[': 'LBRACKET',
            r'\)': 'RPAREN',
            r'\+': 'PLUS',
            r'-=': 'MINUSEQUAL',
            r'=': 'EQUALS',
            r'\{': 'LBRACE',
            r'!=': 'NEQ',
            r'\(': 'LPAREN',
            r'\?': 'OR',
            r'%=': 'PERCENTEQUAL',
            r'\~': 'TILDE',
            r'<=': 'LTE',
            r';': 'SEMI',
            r',': 'COMMA',
            r'%': 'PERCENT',
            r'>=': 'GTE',
            r'_': 'UNDERSCORE',
            r'!!': 'NOT',
            r'<': 'LT',
            r'==': 'EQ',
            r'/=': 'SLASHEQUAL',
            r'\*=': 'STAREQUAL',
            r'>': 'GT',
            r'-': 'MINUS',
            r'\*': 'STAR',
            r'/': 'SLASH',
        }
        for sym, sym_token in symbols.items():
            self.lexer.add(sym_token, sym)

        # Whitespace
        self.lexer.add('WHITESPACE', r'\s+')

        # Identifier and Literals
        self.lexer.add('IDENTIFIER', r'[a-z][a-zA-Z0-9_]*')
        self.lexer.add('PASTALITERAL', r'\"(?:\\.|[^"\\])*\"')
        self.lexer.add('SKIMLITERAL', r'\d*\.\d+|\d+\.\d*')
        self.lexer.add('PINCHLITERAL', r'\d+')
        self.lexer.add('BOOLITERAL',r'True,False')

        self.lexer.ignore(r'#.*')

    def tokenize(self, text):
        """
        Tokenize the input text and handle potential lexical errors
        """
        self._add_tokens()
        lexer = self.lexer.build()
        
        self.tokens = []
        self.errors = []
        
        pos = Position(0, 0, 0, self.fn, text)
        
        try:
            # Tokenize
            for token in lexer.lex(text):
            
                self.tokens.append((token.value, token.name, pos.copy()))
                
                # positions
                for char in token.value:
                    pos.advance(char)
        
        except Exception as e:
            # Handle any unexpected lexical errors
            error_pos = pos.copy()
            self.errors.append(IllegalCharError(
                error_pos, 
                error_pos, 
                f"Unexpected error during tokenization: {str(e)}"
            ))
        
        # Validate tokens
        self._validate_tokens(text)
        
        return self.tokens, self.errors

    def _validate_tokens(self, text):
        """
        Additional validation for tokens
        """
        # Check for invalid identifiers
        for i, (value, token_type, pos) in enumerate(self.tokens):
            if token_type == 'IDENTIFIER':
                # Check identifier length or other rules
                if len(value) > 20: 
                    error = InvalidIdentifierError(
                        pos, 
                        pos, 
                        f"Identifier '{value}' exceeds maximum length of 20 characters"
                    )
                    self.errors.append(error)
        
        # Check for unterminated strings
        for i, (value, token_type, pos) in enumerate(self.tokens):
            if token_type == 'PASTALITERAL':
                if not (value.startswith('"') and value.endswith('"')):
                    error = UnterminatedStringError(
                        pos, 
                        pos, 
                        f"Unterminated string literal: {value}"
                    )
                    self.errors.append(error)
        
        # New validation: Ensure code is between DINEIN and TAKEOUT
        found_dinein = False
        found_takeout = False
        
        for i, (value, token_type, pos) in enumerate(self.tokens):
            if token_type == 'DINEIN':
                found_dinein = True
            
            if token_type == 'TAKEOUT':
                found_takeout = True
            
            # If tokens exist before DINEIN or after TAKEOUT, add an error
            if not found_dinein and token_type not in ['WHITESPACE']:
                self.errors.append(IllegalCharError(
                    pos, 
                    pos, 
                    "Code must start with 'dinein' keyword"
                ))
            
            if found_takeout and token_type not in ['WHITESPACE', 'TAKEOUT']:
                self.errors.append(IllegalCharError(
                    pos, 
                    pos, 
                    "Code must end with 'takeout' keyword"
                ))
        
        # Additional check to ensure both DINEIN and TAKEOUT are present
        if not found_dinein or not found_takeout:
            self.errors.append(IllegalCharError(
                pos, 
                pos, 
                "Code must be enclosed between 'dinein' and 'takeout' keywords"
            ))

    def get_lexer(self):
        self._add_tokens()
        return self.lexer.build()