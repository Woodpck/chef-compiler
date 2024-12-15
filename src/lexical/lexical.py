class LexicalAnalyzer:
    def __init__(self):
        self.tokens = []
        self.errors = []
        # self.whitespace = {' ', '\t', '\n'}

        # self.alpha_big = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        # self.alpha_small = set("abcdefghijklmnopqrstuvwxyz")
        # self.all_num = set("0123456789")
        # self.all_alpha = self.alpha_small | self.alpha_big
        # self.alpha_num = self.all_alpha | self.all_num
        # self.bool_delim = {';' , ' ' , ')'}

        self.asciicmnt = {chr(i) for i in range(32, 127) if chr(i) not in {'/', '-'}}
        self.asciistr = {chr(i) for i in range(32, 127) if chr(i) != '"'}
        self.strdelim = {',', ';', ' ', ':', ')', '}', '+'}
        self.letterdelim = {' ', ';', ',', ':', '}', ')'}
        # self.semicolon_delim = {';'}
        # self.colon_delim = {':'}
        
        #CHEFSCRIPT DELIMITERS
        
        self.whitespace = {' ', '\t', '\n'}

        self.alpha_big = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        self.alpha_small = set("abcdefghijklmnopqrstuvwxyz")
        self.all_num = set("0123456789")
        self.all_alpha = self.alpha_small | self.alpha_big
        self.alpha_num = self.all_alpha | self.all_num
        
        ##Escape Sequnce Delimiter
        self.tab_delim = {'\t'}
        self.newline_delim ={'\n'}
        
        ##Identifier Delimiter
        #self.id_delim = {'\n', ' ', '+', '<', '/', '&', '[', '-', '?', '>', ';', '(', '*', '%', '=', '!', '~', ')', '\t','"', '”'} | self.delim10 | self.all_alpha | self.all_num
        
        ##Other Delimiter
        # Initialize required sets
        self.alpha_num = self.all_alpha | self.all_num  # Alphanumeric characters
        self.newline_delim = {'\n'}  # Newline delimiter
        self.tab_delim = {'\t'}  # Tab delimiter
        self.arith_delim = {'+', '-', '*', '/', '%'}  # Arithmetic operators
        self.assign_delim = {'='}  # Assignment operator
        self.rel_delim = {'<', '>', '<=', '>='}  # Relational operators
        self.logi_delim = {'&&', '||', '!'}  # Logical operators

# Fixing delimiters
        self.num_delim = {' ', '?', '+', '{', '>', '-', ';', '[', ')', '!', '<', '*', '/', '=', '~', '%', '(', ']', ','}
        self.dt_delim = {' ', '\t'}
        self.pasta_delim = self.all_alpha | self.all_num
        self.space_delim = {' '}
        self.bool_delim = {';', '('} | self.space_delim
        self.opdelim = {'+', '-', '*', '/', '%', '**'}
        self.oparan_delim = {'('}
        self.cparan_delim = {')'}
        self.id_delim = {' ', ';', ',', '.', '(', ')', '{', '[', ']'} | self.opdelim
        self.digdelim = {' ', ';', ':', ',', '}', ')', ']'} | self.opdelim
        self.pardelim = {'('}
        self.delim0 = {' ', '('}
        self.delim1 = {';', ')', ' ', '“', ',”', '}', '!', '=', '&', '?', '<', '>'}
        self.delim2 = {'{'} | self.space_delim
        self.delim3 = set()  # Empty set
        self.delim4 = self.space_delim | self.alpha_num
        self.delim5 = {'!'} | self.delim4 | self.space_delim
        self.delim6 = {'"', '!', '('} | self.space_delim | self.delim4
        self.delim7 = {'!', '('} | self.space_delim | self.delim4
        self.delim8 = self.space_delim | self.all_alpha
        self.delim9 = self.space_delim | self.newline_delim | self.tab_delim
        self.delim10 = self.arith_delim | self.assign_delim | self.rel_delim | self.logi_delim | self.all_alpha | self.alpha_num

        
        ##Reserve Symbols Delimiter
        self.arith_delim = {'+', '-', '*', '/', '%'}
        self.assign_delim = {'=', '+=', '-=', '*=', '/=', '%='}
        self.rel_delim = {'==', '!=', '<', '>', '<=', '>='}
        self.logi_delim = {'&&', '??', '!!'}
        
        ##Other Delimiter
        self.comma_delim = {','}
        self.semicolon_delim_delim = {','}
        self.colon_delim = {':'}
        self.otherOp_delim = {'+', '!'}
        self.oparan_delim = {'('}
        self.cparan_delim = {')'}
        self.obrack_delim = {'['}
        self.cbrack_delim = {']'}
        self.ocurlyb_delim = {'{'}
        self.ccurlyb_delim = {'}'}
        # self.multicom_delim = {' \--\ '}
        # self.singlecom_delim = {'\\'}
        
        #CHEFSCRIPT DELIMITERS
        
        # self.dtdelim = {' '}
        # self.delim0 = {' ', '('}
        # self.delim1 = { }
        # self.delim2 = {' ', ')', ';', ','}
        # self.delim3 = {' ', ';', ')'} | self.all_alpha
        # self.delim4 = {' ', '~', '('} | self.all_alpha
        # self.delim5 = {' ', '\n'}
        # self.delim6 = {' ', '"', '('} | self.all_alpha
        # self.delim7 = {' ', '\n'}
        # self.delim8 = {'\n'}
        # self.delim9 = {' ', '~', '"', '\'', '('} | self.all_alpha
        # self.delim10 = {'"', '~', '\'', ' '} | self.all_alpha
        # self.delim12 = {')', '!', '\'', '"', ' '} | self.all_alpha
        # self.delim13 = {';', '{', ')', '<', '>', '=', '|', '&', '+', '-', '/', '*', '%', ' '}
        # self.delim14 = {']', ' '} | self.all_alpha
        # self.delim15 = {'=', ';', ' ', '\n', '['}
        # self.delim16 = {'\'', '"', '~', ' ', '\n', '{'} | self.all_alpha
        # self.delim17 = {';', '}', ',', ' ', '\n'} | self.alpha_big
        
        self.errors = []
        self.code = ""
        self.index = 0
        self.line_number = 1

    def nextChar(self):
            if self.index < len(self.code):
                c = self.code[self.index]
                self.index += 1
                return c
            return None
        
    def stepBack(self):
            if self.index > 0:
                self.index -= 1

    def tokenize(self, code):
        self.code = code
        tokens = []
        self.index = 0
        state = 0
        lexeme = ""
        line = 1

        while True:
            c = self.nextChar()

            if c is None and state == 0:
                break
            
            print(f"State: {state}, char: {repr(c)}, Lexeme: {repr(lexeme)}, Line: {line}")
            
            match state:
                case 0:
                    lexeme = ""
                    
                    if c == 'b':
                        state = 1
                        lexeme += 'b'
                    elif c == 'c':
                        state = 10
                        lexeme += 'c'
                    elif c == 'd':
                        state = 22
                        lexeme += 'd'
                    elif c == 'e':
                        state = 39
                        lexeme += 'e'
                    elif c == 'f':
                        state = 44
                        lexeme += 'f'
                    elif c == 'h':
                        state = 56
                        lexeme += 'h'
                    elif c == 'k':
                        state = 63
                        lexeme += 'k'
                    elif c == 'm':
                        state = 71
                        lexeme += 'm'
                    elif c == 'p':
                        state = 79
                        lexeme += 'p'
                    elif c == 'r':
                        state = 90
                        lexeme += 'r'
                    elif c == 's':
                        state = 97
                        lexeme += 's'
                    elif c == 't':
                        state = 117
                        lexeme += 't'
                    elif c == 'y':
                        state = 129
                        lexeme += 'y'
                    elif c == ' ':
                        state = 133
                        lexeme += ' '
                    elif c == '\t':
                        state = 135
                        lexeme += '\t'
                    elif c == '\n':
                        state = 137
                        lexeme += '\n'
                        line += 1
                    elif c == '-':
                        state = 139
                        lexeme += '-'
                    elif c == '.':
                        state = 145
                        lexeme += '.'
                    elif c == '!':
                        state = 147
                        lexeme += '!'
                    elif c == '?':
                        state = 153
                        lexeme += '?'
                    elif c == '(':
                        state = 156
                        lexeme += '('
                    elif c == ')':
                        state = 158
                        lexeme += ')'
                    elif c == '[':
                        state = 160
                        lexeme += '['
                    elif c == ']':
                        state = 162
                        lexeme += ']'
                    elif c == '{':
                        state = 164
                        lexeme += '{'
                    elif c == '}':
                        state = 166
                        lexeme += '}'
                    elif c == '*':
                        state = 168
                        lexeme += '*'
                    elif c == '/':
                        state = 172
                        lexeme += '/'
                    elif c == '&':
                        state = 180
                        lexeme += '&'
                    elif c == '%':
                        state = 183
                        lexeme += '%'
                    elif c == '+':
                        state = 187
                        lexeme += '+'
                    elif c == '<':
                        state = 193
                        lexeme += '<'
                    elif c == '=':
                        state = 197
                        lexeme += '='
                    elif c == '>':
                        state = 201
                        lexeme += '>'
                    elif c == '"':
                        state = 205
                        lexeme += '"'
                    elif c == '~':
                        state = 208
                        lexeme += c  
                    elif c in self.all_num:
                        state = 209
                        lexeme += c 
                        
                    elif c in self.alpha_small:
                        state = 230
                        lexeme += c
                    
                
                case 1:
                    if c == 'l':
                        state = 2
                        lexeme += c
                    elif c == 'o':
                        state = 6
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 2:
                    if c == 'e':
                        state = 3
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                
                case 3:
                    if c == 'h':
                        state = 4
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                    
                case 4:
                    if c in self.bool_delim:
                        state = 5
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 5:
                    tokens.append((lexeme, "bleh"))
                    if c is not None:
                        self.stepBack()
                    state = 0
                    
                case 6:
                    if c == 'o':
                        state = 7
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                
                case 7:
                    if c == 'l':
                        state = 8
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 8:
                    if c in self.bool_delim:
                        state = 9
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                
                case 9:
                    tokens.append((lexeme, "bool"))
                    if c is not None:
                        self.stepBack()
                    state = 0
                
                case 10:
                    if c == 'a':
                        state = 11
                        lexeme += c
                    elif c == 'h':
                        state = 15
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                    
                case 11:
                    if c == 's':
                        state = 12
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 12:
                    if c == 'e':
                        state = 13
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                
                case 13:
                    if c in self.delim4:
                        state = 14
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 14:
                    tokens.append((lexeme, "case"))
                    if c is not None:
                        self.stepBack()
                    state = 0
                
                case 15:
                    if c == 'e':
                        state = 16
                        lexeme += c
                    elif c == 'o':
                        state = 19
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0

                case 16:
                    if c == 'f':
                        state = 17
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                
                case 17:
                    if c in self.space_delim:
                        state = 18
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                
                case 18:
                    tokens.append((lexeme, "chef"))
                    if c is not None:
                        self.stepBack()
                    state = 0
                
                case 19:
                    if c == 'p':
                        state = 20
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                
                case 20:
                    if c in self.semicolon_delim:
                        state = 21
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 21:
                    tokens.append((lexeme, "chop"))
                    if c is not None:
                        self.stepBack()
                    state = 0
                    
                case 22:
                    if c == 'e':
                        state = 23
                        lexeme += c
                    elif c == 'i':
                        state = 30
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 23:
                    if c == 'f':
                        state = 24
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 24:
                    if c == 'a':
                        state = 25
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 25:
                    if c == 'u':
                        state = 26
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 26:
                    if c == 'l':
                        state = 27
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 27:
                    if c == 't':
                        state = 28
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 28:
                    if c in self.colon_delim:
                        state = 29
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 29:
                    tokens.append((lexeme, "default"))
                    if c is not None:
                        self.stepBack()
                    state = 0
                    
                case 30:
                    if c == 'n':
                        state = 31
                        lexeme += c
                    elif c == 's':
                        state = 36
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                
                case 31:
                    if c == 'e':
                        state = 32
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                
                case 32:
                    if c == 'i':
                        state = 33
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 33:
                    if c == 'n':
                        state = 34
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                    
                case 34:
                    if c in self.newline_delim:
                        state = 35
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 35:
                    tokens.append((lexeme, "dinein"))
                    if c is not None:
                        self.stepBack()
                    state = 0
                    
                case 36:
                    if c == 'h':
                        state = 37
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 37:
                    if c in self.oparan_delim:
                        state = 38
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                
                case 38:
                    tokens.append((lexeme, "dish"))
                    if c is not None:
                        self.stepBack()
                    state = 0
                
                case 39:
                    if c == 'l':
                        state = 40
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 40:
                    if c == 'i':
                        state = 41
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                
                case 41:
                    if c == 'f':
                        state = 42
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 42:
                    if c in self.delim0:
                        state = 43
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                
                case 43:
                    tokens.append((lexeme, "elif"))
                    if c is not None:
                        self.stepBack()
                    state = 0
                    
                case 44:
                    if c == 'l':
                        state = 45
                        lexeme += c
                    elif c == 'o':
                        state = 49
                        lexeme += c
                    elif c == 'u':
                        state = 52
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 45:
                    if c == 'i':
                        state = 46
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 46:
                    if c == 'p':
                        state = 47
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 47:
                    if c in self.delim0:
                        state = 48
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 48:
                    tokens.append((lexeme, "flip"))
                    if c is not None:
                        self.stepBack()
                    state = 0
                    
                case 49:
                    if c == 'r':
                        state = 50
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 50:
                    if c in self.delim0:
                        state = 51
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 51:
                    tokens.append((lexeme, "for"))
                    if c is not None:
                        self.stepBack()
                    state = 0
                    
                case 52:
                    if c == 'l':
                        state = 53
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 53:
                    if c == 'l':
                        state = 54
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 54:
                    if c in self.dt_delim:
                        state = 55
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 55:
                    tokens.append((lexeme, "full"))
                    if c is not None:
                        self.stepBack()
                    state = 0
                    
                case 56:
                    if c == 'u':
                        state = 57
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 57:
                    if c == 'n':
                        state = 58
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 58:
                    if c == 'g':
                        state = 59
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 59:
                    if c == 'r':
                        state = 60
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 60:
                    if c == 'y':
                        state = 61
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 61:
                    if c in self.space_delim:
                        state = 62
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 62:
                    tokens.append((lexeme, "hungry"))
                    if c is not None:
                        self.stepBack()
                    state = 0
                    
                case 63:
                    if c == 'e':
                        state = 64
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 64:
                    if c == 'e':
                        state = 65
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 65:
                    if c == 'p':
                        state = 66
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 66:
                    if c == 'm':
                        state = 67
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                    
                case 67:
                    if c == 'i':
                        state = 68
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 68:
                    if c == 'x':
                        state = 69
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 69:
                    if c in self.delim2:
                        state = 70
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 70:
                    tokens.append((lexeme, "keepmix"))
                    if c is not None:
                        self.stepBack()
                    state = 0
                    
                case 71:
                    if c == 'a':
                        state = 72
                        lexeme += c
                    elif c == 'i':
                        state = 76
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 72:
                    if c == 'k':
                        state = 73
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 73:
                    if c == 'e':
                        state = 74
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 74:
                    if c in self.delim0:
                        state = 75
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 75:
                    tokens.append((lexeme, "make"))
                    if c is not None:
                        self.stepBack()
                    state = 0
                    
                case 76:
                    if c == 'x':
                        state = 77
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 77:
                    if c in self.delim2:
                        state = 78
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 78:
                    tokens.append((lexeme, "mix"))
                    if c is not None:
                        self.stepBack()
                    state = 0
                        
                case 79:
                    if c == 'a':
                        state = 80
                        lexeme += c
                    elif c == 'i':
                        state = 85
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 80:
                    if c == 's':
                        state = 81
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 81:
                    if c == 't':
                        state = 82
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 82:
                    if c == 'a':
                        state = 83
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 83:
                    if c in self.dt_delim:
                        state = 84
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 84:
                    tokens.append((lexeme, "pasta"))
                    if c is not None:
                        self.stepBack()
                    state = 0
                    
                case 85:
                    if c == 'n':
                        state = 86
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 86:
                    if c == 'c':
                        state = 87
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 87:
                    if c == 'h':
                        state = 88
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                    
                case 88:
                    if c in self.dt_delim:
                        state = 89
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 89:
                    tokens.append((lexeme, "pinch"))
                    if c is not None:
                        self.stepBack()
                    state = 0
                        
                case 90:
                    if c == 'e':
                        state = 91
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 91:
                    if c == 'c':
                        state = 92
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 92:
                    if c == 'i':
                        state = 93
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 93:
                    if c == 'p':
                        state = 94
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 94:
                    if c == 'e':
                        state = 95
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 95:
                    if c in self.dt_delim:
                        state = 96
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 96:
                    tokens.append((lexeme, "recipe"))
                    if c is not None:
                        self.stepBack()
                    state = 0
                
                case 97:
                    if c == 'e':
                        state = 98
                        lexeme += c
                    elif c == 'i':
                        state = 103
                        lexeme += c
                    elif c == 'k':
                        state = 109
                        lexeme += c
                    elif c == 'p':
                        state = 113
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 98:
                    if c == 'r':
                        state = 99
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 99:
                    if c == 'v':
                        state = 100
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 100:
                    if c == 'e':
                        state = 101
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                
                case 101:
                    if c in self.delim0:
                        state = 102
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 102:
                    tokens.append((lexeme, "serve"))
                    if c is not None:
                        self.stepBack()
                    state = 0
                    
                case 103:
                    if c == 'm':
                        state = 104
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 104:
                    if c == 'm':
                        state = 105
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                
                case 105:
                    if c == 'e':
                        state = 106
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 106:
                    if c == 'r':
                        state = 107
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 107:
                    if c in self.delim0:
                        state = 108
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 108:
                    tokens.append((lexeme, "simmer"))
                    if c is not None:
                        self.stepBack()
                    state = 0
                        
                case 109:
                    if c == 'i':
                        state = 110
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 110:
                    if c == 'm':
                        state = 111
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 111:
                    if c in self.dt_delim:
                        state = 112
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 112:
                    tokens.append((lexeme, "skim"))
                    if c is not None:
                        self.stepBack()
                    state = 0
                    
                case 113:
                    if c == 'i':
                        state = 114
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 114:
                    if c == 't':
                        state = 115
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 115:
                    if c in self.space_delim:
                        state = 116
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 116:
                    tokens.append((lexeme, "spit"))
                    if c is not None:
                        self.stepBack()
                    state = 0
                    
                case 117:
                    if c == 'a':
                        state = 118
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                    
                case 118:
                    if c == 'k':
                        state = 119
                        lexeme += c
                    elif c == 's':
                        state = 125
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 119:
                    if c == 'e':
                        state = 120
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 120:
                    if c == 'o':
                        state = 121
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 121:
                    if c == 'u':
                        state = 122
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 122:
                    if c == 't':
                        state = 123
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 123:
                    if c in self.delim9:
                        state = 124
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 124:
                    tokens.append((lexeme, "takeout"))
                    if c is not None:
                        self.stepBack()
                    state = 0
                    
                case 125:
                    if c == 't':
                        state = 126
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 126:
                    if c == 'e':
                        state = 127
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 127:
                    if c in self.delim0:
                        state = 128
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 128:
                    tokens.append((lexeme, "taste"))
                    if c is not None:
                        self.stepBack()
                    state = 0
                    
                case 129:
                    if c == 'u':
                        state = 130
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                    
                case 130:
                    if c == 'm':
                        state = 131
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                    
                case 131:
                    if c in self.bool_delim:
                        state = 132
                        lexeme += c
                    elif c and (c.isalpha() or c.isdigit() or c == '_'):
                        state = 232
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 132:
                    tokens.append((lexeme, "yum"))
                    if c is not None:
                        self.stepBack()
                    state = 0
                case 133:
                    if c in self.space_delim:
                        state = 134
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 134:
                    tokens.append((lexeme, " "))
                    if c is not None:
                        self.stepBack()
                    state = 0
                    
                case 135:
                    if c in self.tab_delim:
                        state = 136
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 136:
                    tokens.append((lexeme, "\t"))
                    if c is not None:
                        self.stepBack()
                    state = 0
                    
                case 137:
                    if c in self.newline_delim:
                        state = 138
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 138:
                    tokens.append((lexeme, "\n"))
                    if c is not None:
                        self.stepBack()
                    state = 0
                    
                case 139:
                    if c in self.arith_delim:
                        state = 140
                        lexeme += c
                    elif c == '-':
                        state = 141
                        lexeme += c
                    elif c == '=':
                        state = 143
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 140:
                    tokens.append((lexeme, "-"))
                    if c is not None:
                        self.stepBack()
                    state = 0
                    
                case 141:
                    if c in self.otherOp_delim:
                        state = 142
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                
                case 142:
                    tokens.append((lexeme, "--"))
                    if c is not None:
                        self.stepBack()
                    state = 0
                    
                case 143:
                    if c in self.assign_delim:
                        state = 144
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                
                case 144:
                    tokens.append((lexeme, "-="))
                    if c is not None:
                        self.stepBack()
                    state = 0
                
                case 145:
                    if c in self.comma_delim:
                        state = 146
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 146:
                    tokens.append((lexeme, ","))
                    if c is not None:
                        self.stepBack()
                    state = 0
                    
                case 147:
                    if c in self.otherOp_delim:
                        state = 148
                        lexeme += c
                    elif c == '!':
                        state = 149
                        lexeme += c
                    elif c == '=':
                        state = 151
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 148:
                    tokens.append((lexeme, "!"))
                    if c is not None:
                        self.stepBack()
                    state = 0
                    
                case 149:
                    if c in self.logi_delim:
                        state = 150
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 150:
                    tokens.append((lexeme, "!!"))
                    if c is not None:
                        self.stepBack()
                    state = 0
                
                case 151:
                    if c in self.rel_delim:
                        state = 152
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 152:
                    tokens.append((lexeme, "!="))
                    if c is not None:
                        self.stepBack()
                    state = 0
                        
                case 153:
                    if c == '?':
                        state = 154                        
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 154:
                    if c in self.logi_delim:
                        state = 155
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 155:
                    tokens.append((lexeme, "?"))
                    if c is not None:
                        self.stepBack()
                    state = 0
                    
                case 156:
                    if c in self.oparan_delim:
                        state = 157
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 157:
                    tokens.append((lexeme, "("))
                    if c is not None:
                        self.stepBack()
                    state = 0
                    
                case 158:
                    if c in self.cparan_delim:
                        state = 159
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 159:
                    tokens.append((lexeme, ")"))
                    if c is not None:
                        self.stepBack()
                    state = 0
                    
                case 160:
                    if c in self.obrack_delim:
                        state = 161
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 161:
                    tokens.append((lexeme, "["))
                    if c is not None:
                        self.stepBack()
                    state = 0
                    
                case 162:
                    if c in self.cbrack_delim:
                        state = 163
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 163:
                    tokens.append((lexeme, "]"))
                    if c is not None:
                        self.stepBack()
                    state = 0
                    
                case 164:
                    if c in self.ocurlyb_delim:
                        state = 165
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 165:
                    tokens.append((lexeme, "{"))
                    if c is not None:
                        self.stepBack()
                    state = 0
                    
                case 166:
                    if c in self.ccurlyb_delim:
                        state = 167
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 167:
                    tokens.append((lexeme, "}"))
                    if c is not None:
                        self.stepBack()
                    state = 0
                  
                case 168:
                    if c in self.arith_delim:
                        state = 169
                        lexeme += c
                    elif c == '=':
                        state = 170
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 169:
                    tokens.append((lexeme, "*"))
                    if c is not None:
                        self.stepBack()
                    state = 0  
                    
                case 170:
                    if c in self.assign_delim:
                        state = 171
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 171:
                    tokens.append((lexeme, "*="))
                    if c is not None:
                        self.stepBack()
                    state = 0 
                    
                case 172:
                    if c in self.arith_delim:
                        state = 173
                        lexeme += c
                    elif c == '/':
                        state = 174
                        lexeme += c
                    elif c == '-':
                        state = 176
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 173:
                    tokens.append((lexeme, "/"))
                    if c is not None:
                        self.stepBack()
                    state = 0
                    
                case 174:
                    if c in self.asciicmnt:
                        state = 174
                        lexeme += c
                    elif c in self.singlecom_delim:
                        state = 175
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 175:
                    if c is not None:
                        self.stepBack()
                    state = 0
                    
                case 176:
                    if c in self.asciicmnt:
                        state = 176
                        lexeme += c
                    elif c == '-':
                        state = 177
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                    
                case 177:
                    if c == '/':
                        state = 178
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 178:
                    if c in self.multicom_delim:
                        state = 179
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 179:
                    if c is not None:
                        self.stepBack()
                    state = 0
                    
                case 180:
                    if c == '&':
                        state = 181
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 181:
                    if c in self.logi_delim:
                        state = 182
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 182:
                    tokens.append((lexeme, "&&"))
                    if c is not None:
                        self.stepBack()
                    state = 0
                
                case 183:
                    if c in self.arith_delim:
                        state = 184
                        lexeme += c
                    elif c == '=':
                        state = 185
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                    
                case 184:
                    tokens.append((lexeme, "%"))
                    if c is not None:
                        self.stepBack()
                    state = 0
                    
                case 185:
                    if c in self.assign_delim:
                        state = 186
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 186:
                    tokens.append((lexeme, "%="))
                    if c is not None:
                        self.stepBack()
                    state = 0
                    
                case 187:
                    if c in self.arith_delim:
                        state = 188
                        lexeme += c
                    elif c == '+':
                        state = 189
                        lexeme += c
                    elif c == '=':
                        state = 191
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                
                case 188:
                    tokens.append((lexeme, "+"))
                    if c is not None:
                        self.stepBack()
                    state = 0
                    
                case 189:
                    if c in self.otherOp_delim:
                        state = 190
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 190:
                    tokens.append((lexeme, "++"))
                    if c is not None:
                        self.stepBack()
                    state = 0
                    
                case 191:
                    if c in self.assign_delim:
                        state = 192
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 192:
                    tokens.append((lexeme, "+="))
                    if c is not None:
                        self.stepBack()
                    state = 0
                
                case 193:
                    if c in self.rel_delim:
                        state = 194
                        lexeme += c
                    elif c == '=':
                        state = 195
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                
                case 194:
                    tokens.append((lexeme, "<"))
                    if c is not None:
                        self.stepBack()
                    state = 0
                    
                case 195:
                    if c in self.rel_delim:
                        state = 196
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 196:
                    tokens.append((lexeme, "<="))
                    if c is not None:
                        self.stepBack()
                    state = 0
                    
                case 197:
                    if c in self.assign_delim:
                        state = 198
                        lexeme += c
                    elif c == '=':
                        state = 199
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 198:
                    tokens.append((lexeme, "="))
                    if c is not None:
                        self.stepBack()
                    state = 0
                    
                case 199:
                    if c in self.rel_delim:
                        state = 200
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 200:
                    tokens.append((lexeme, "=="))
                    if c is not None:
                        self.stepBack()
                    state = 0
                    
                case 201:
                    if c in self.rel_delim:
                        state = 202
                        lexeme += c
                    elif c == '=':
                        state = 203
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 202:
                    tokens.append((lexeme, ">"))
                    if c is not None:
                        self.stepBack()
                    state = 0
                    
                case 203:
                    if c in self.rel_delim:
                        state = 204
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 204:
                    tokens.append((lexeme, ">="))
                    if c is not None:
                        self.stepBack()
                    state = 0
                    
                    
                case 205:
                    if c in self.asciistr:
                        state = 205
                        lexeme += c
                    elif c == '"':
                        state = 206
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 206:
                    if c in self.pasta_delim:
                        state = 207
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 207:
                    tokens.append((lexeme, '"'))
                    if c is not None:
                        self.stepBack()
                    state = 0


                #pinch and skim
                case 208:
                    if c in self.all_num:
                        state = 209
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                case 209:
                    if c in self.all_num:
                        state = 210
                        lexeme += c
                    elif c == '.':
                        state = 219
                        lexeme += c
                    elif c == '.':
                        state = 219
                        lexeme += c
                    elif c in self.delim10:
                        state = 218
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                case 210:
                    if c in self.all_num:
                        state = 211
                        lexeme += c
                    elif c == '.':
                        state = 219
                        lexeme += c
                    elif c in self.delim10:
                        state = 218
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                case 211:
                    if c in self.all_num:
                        state = 212
                        lexeme += c
                    elif c == '.':
                        state = 219
                        lexeme += c
                    elif c in self.delim10:
                        state = 218
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                case 212:
                    if c in self.all_num:
                        state = 213
                        lexeme += c
                    elif c == '.':
                        state = 219
                        lexeme += c
                    elif c in self.delim10:
                        state = 218
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0       
                case 213:
                    if c in self.all_num:
                        state = 214
                        lexeme += c
                    elif c == '.':
                        state = 219
                        lexeme += c
                    elif c in self.delim10:
                        state = 218
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0    
                case 214:
                    if c in self.all_num:
                        state = 215
                        lexeme += c
                    elif c == '.':
                        state = 219
                        lexeme += c
                    elif c in self.delim10:
                        state = 218
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0    
                case 215:
                    if c in self.all_num:
                        state = 216
                        lexeme += c
                    elif c == '.':
                        state = 219
                        lexeme += c
                    elif c in self.delim10:
                        state = 218
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0    
                case 216:
                    if c in self.all_num:
                        state = 217
                        lexeme += c
                    elif c == '.':
                        state = 219
                        lexeme += c
                    elif c in self.delim10:
                        state = 218
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                case 217:
                    if c == '.':
                        state = 219
                        lexeme += c
                    elif c in self.delim10:
                        state = 218
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0  
                case 218:
                    tokens.append((lexeme, "pinch literal"))
                    if c is not None:
                        self.stepBack()
                    state = 0
                case 219:
                    if c in self.all_num:
                        state = 220
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0      
                case 220:
                    if c in self.all_num:
                        state = 221
                        lexeme += c
                    elif c in self.delim10:
                        state = 229
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0 
                case 221:
                    if c in self.all_num:
                        state = 222
                        lexeme += c
                    elif c in self.delim10:
                        state = 229
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                case 222:
                    if c in self.all_num:
                        state = 223
                        lexeme += c
                    elif c in self.delim10:
                        state = 229
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0 
                case 223:
                    if c in self.all_num:
                        state = 224
                        lexeme += c
                    elif c in self.delim10:
                        state = 229
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0   
                case 224:
                    if c in self.all_num:
                        state = 225
                        lexeme += c
                    elif c in self.delim10:
                        state = 229
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                case 225:
                    if c in self.all_num:
                        state = 226
                        lexeme += c
                    elif c in self.delim10:
                        state = 229
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                case 226:
                    if c in self.all_num:
                        state = 227
                        lexeme += c
                    elif c in self.delim10:
                        state = 229
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                case 227:
                    if c in self.all_num:
                        state = 228
                        lexeme += c
                    elif c in self.delim10:
                        state = 229
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                case 228:
                    if c in self.delim10:
                        state = 229
                        lexeme += c
                    else:
                        self.errors.append(f"Line {line}: '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                case 229:
                    tokens.append((lexeme, "skim literal"))
                    if c is not None:
                        self.stepBack()
                    state = 0

                #Identifier
                case 230:
                    if c and (c.isalpha() or c.isdigit() or c == '_'):
                        lexeme += c
                        state = 232                        
                    elif c in self.id_delim:
                        state = 231
                        if c is not None:
                            self.stepBack()
                    else:
                        self.errors.append(f"Line {line}: Identifier '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                        
                case 231:
                    tokens.append((lexeme, "identifier"))
                    if c is not None:
                        self.stepBack()
                    state = 0
                    
                case 232:
                    if c and (c.isalpha() or c.isdigit() or c == '_'):
                        lexeme += c
                        
                        if len(lexeme) > 20:
                            self.errors.append(f"Line {line}: Identifier '{lexeme}' exceeds 20 characters.")
                            state = 0

                    elif c in self.id_delim:
                        state = 233
                        if c is not None:
                            self.stepBack()
                    
                    else:
                        if c is None:
                            self.errors.append(f"Line {line}: Identifier '{lexeme}' Invalid Delimiter.")
                        else:
                            self.errors.append(f"Line {line}: Identifier '{lexeme}' Invalid Delimiter ' {repr(c)} '.")
                        state = 0
                
                case 233:
                    tokens.append((lexeme, "identifier"))
                    if c is not None:
                        self.stepBack()
                    state = 0 
                    
        return tokens
     

    def display_tokens(self, tokens):
            print(f"{'Lexeme'.ljust(40)}{'Token'.ljust(20)}")
            print("-" * 60)
            for lexeme, token in tokens:
                print(f"{lexeme.ljust(40)}{token.ljust(20)}")
                print("-" * 60)


    def display_errors(self):
        if self.errors:
            print("\nLexical Errors:\n")
            for error in self.errors:
                    print(error)

    
if __name__ == "__main__": 
    try:
        with open("chef/program", "r") as file:
            code = file.read()
    except FileNotFoundError:
        print("Error: The file 'program' was not found in the current directory.")
        exit(1)

    analyzer = LexicalAnalyzer()
    tokens = analyzer.tokenize(code)

    analyzer.display_tokens(tokens)
    analyzer.display_errors()
    print("\nEnd of program analysis.\n")   