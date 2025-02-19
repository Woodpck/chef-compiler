class SyntaxAnalyzer:
    def __init__(self):
        self.tokens = []
        self.current_index = 0
        self.current_token = None
        self.last_reserved_word = None
        
    def parse(self, tokens):
        self.tokens = tokens
        self.current_index = 0
        self.current_token = self.tokens[0] if tokens else None
        
        try:
            self.parse_program()
            print("Syntax Analysis Successful!")
            return True
        except SyntaxError as e:
            print(f"Syntax Error: {str(e)}")
            return False
            
    def consume(self, expected_token=None):
        if expected_token and self.current_token != expected_token:
            raise SyntaxError(f"Expected {expected_token}, got {self.current_token}")
            
        self.current_index += 1
        if self.current_index < len(self.tokens):
            self.current_token = self.tokens[self.current_index]
        else:
            self.current_token = None
            
    def parse_program(self):
        # Program can have multiple declarations and statements
        while self.current_token:
            if self.current_token in ['pasta', 'pinch', 'skim', 'bool']:
                self.parse_declaration()
            elif self.current_token == 'chef':
                self.parse_main_function()
            elif self.current_token in ['full', 'hungry']:
                self.parse_function_definition()
            else:
                raise SyntaxError(f"Unexpected token {self.current_token}")
                
    def parse_declaration(self):
        # Handle variable declarations
        data_type = self.current_token
        self.consume()
        
        if self.current_token != 'identifier':
            raise SyntaxError("Expected identifier after type")
            
        self.consume()
        
        # Handle multiple declarations
        while self.current_token == ',':
            self.consume()
            if self.current_token != 'identifier':
                raise SyntaxError("Expected identifier after comma")
            self.consume()
            
        if self.current_token == '=':
            self.consume()
            self.parse_expression(data_type)
            
        if self.current_token != ';':
            raise SyntaxError("Expected semicolon")
        self.consume()
        
    def parse_main_function(self):
        # Parse chef (main) function
        self.consume('chef')
        self.consume('pinch')
        self.consume('dish')
        self.consume('(')
        self.consume(')')
        self.consume('{')
        
        self.parse_function_body()
        
        self.consume('}')
        
    def parse_function_definition(self):
        # Parse function definitions (full or hungry)
        func_type = self.current_token
        self.consume()
        
        if self.current_token not in ['pasta', 'pinch', 'skim', 'bool']:
            raise SyntaxError("Expected return type")
            
        return_type = self.current_token
        self.consume()
        
        if self.current_token != 'identifier':
            raise SyntaxError("Expected function name")
        self.consume()
        
        self.parse_parameters()
        self.consume('{')
        self.parse_function_body()
        self.consume('}')
        
    def parse_parameters(self):
        self.consume('(')
        
        if self.current_token in ['pasta', 'pinch', 'skim', 'bool']:
            self.parse_parameter_list()
            
        self.consume(')')
        
    def parse_parameter_list(self):
        self.parse_parameter()
        while self.current_token == ',':
            self.consume()
            self.parse_parameter()
            
    def parse_parameter(self):
        if self.current_token not in ['pasta', 'pinch', 'skim', 'bool']:
            raise SyntaxError("Expected parameter type")
        self.consume()
        
        if self.current_token != 'identifier':
            raise SyntaxError("Expected parameter name")
        self.consume()
        
    def parse_function_body(self):
        while self.current_token and self.current_token != '}':
            if self.current_token in ['pasta', 'pinch', 'skim', 'bool']:
                self.parse_declaration()
            elif self.current_token == 'make':
                self.parse_make_statement()
            elif self.current_token == 'serve':
                self.parse_serve_statement()
            elif self.current_token == 'for':
                self.parse_for_statement()
            elif self.current_token == 'spit':
                self.parse_spit_statement()
            else:
                raise SyntaxError(f"Unexpected token in function body: {self.current_token}")
                
    def parse_make_statement(self):
        self.consume('make')
        self.consume('(')
        self.parse_expression('any')
        self.consume(')')
        self.consume(';')
        
    def parse_serve_statement(self):
        self.consume('serve')
        self.consume('(')
        self.parse_expression('any')
        while self.current_token == '~':
            self.consume()
            self.parse_expression('any')
        self.consume(')')
        self.consume(';')
        
    def parse_for_statement(self):
        self.consume('for')
        self.consume('(')
        
        # Initialize
        if self.current_token not in ['pinch', 'skim']:
            raise SyntaxError("Expected pinch or skim in for loop initialization")
        self.consume()
        if self.current_token != 'identifier':
            raise SyntaxError("Expected identifier in for loop initialization")
        self.consume()
        self.consume('=')
        self.parse_expression('numeric')
        self.consume(';')
        
        # Condition
        self.parse_expression('numeric')
        if self.current_token not in ['<', '>', '<=', '>=', '==', '!=']:
            raise SyntaxError("Expected comparison operator")
        self.consume()
        self.parse_expression('numeric')
        self.consume(';')
        
        # Update
        if self.current_token != 'identifier':
            raise SyntaxError("Expected identifier in for loop update")
        self.consume()
        if self.current_token not in ['+=', '-=']:
            raise SyntaxError("Expected += or -=")
        self.consume()
        self.parse_expression('numeric')
        
        self.consume(')')
        self.consume('{')
        self.parse_function_body()
        self.consume('}')
        
    def parse_spit_statement(self):
        self.consume('spit')
        self.parse_expression('any')
        self.consume(';')
        
    def parse_expression(self, expected_type):
        if self.current_token in ['identifier', 'pastaliterals', 'pinchliterals', 'NEALITERAL', 
                                'skimliterals', 'NEHLITERAL', 'yum', 'bleh']:
            self.consume()
        else:
            raise SyntaxError(f"Invalid expression token: {self.current_token}")
        
# Example usage:
analyzer = SyntaxAnalyzer()

# Sample tokens for a simple program
sample_tokens = [
    'chef', 'pinch', 'dish', '(', ')', '{',
    'pasta', 'identifier', '=', 'pastaliterals', ';',
    'pinch', 'identifier', '=', 'pinchliterals', ';',
    'serve', '(', 'identifier', ')', ';',
    'spit', 'pastaliterals', ';',
    '}'
]

result = analyzer.parse(sample_tokens)