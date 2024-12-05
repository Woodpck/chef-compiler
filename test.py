from rply import LexerGenerator

class Lexer:
    def __init__(self):
        self.lexer = LexerGenerator()

    def _add_tokens(self):
        # Simple tokenization example
        self.lexer.add('NUMBER', r'\d+')
        self.lexer.add('PLUS', r'\+')
        self.lexer.add('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*')
        self.lexer.ignore(r'\s+')

    def analyze_code(self, code):
        self._add_tokens()
        lexer = self.lexer.build()
        
        tokens = []
        error_tokens = []
        
        try:
            for token in lexer.lex(code):
                tokens.append((token.value, token.name))
        except Exception as e:
            error_tokens.append(f"Error during lexing: {str(e)}")
        
        if not tokens and not error_tokens:
            error_tokens.append("No tokens found.")
        
        return tokens, error_tokens

# Test with a valid example
lexer = Lexer()
code = "number = 5 + 3"
tokens, errors = lexer.analyze_code(code)
print("Tokens:", tokens)
print("Errors:", errors)
