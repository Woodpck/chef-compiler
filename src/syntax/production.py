def _add_productions(self):
        @self.pg.production('program : global_declarations functions CHEF PINCH DISH LPAREN RPAREN LBRACE body SPIT PINCHLITERAL SEMI RBRACE')
        def program(p):
            print("parsing program")

        @self.pg.production('global_declarations : declarations')
        def global_declarations(p):
            print("parsing global_declarations")
            

        @self.pg.production('declarations : declares declarations')
        @self.pg.production('declarations : ')
        def declarations(p):
            print("parsing declarations")
            

        @self.pg.production('declares : variable_decls')
        @self.pg.production('declares : stmt')
        @self.pg.production('declares : recipe_decl')
        @self.pg.production('declares : recipe_init')
        @self.pg.production('declares : ')
        def declares(p):
            print("parsing declares")
        

        @self.pg.production('variable_decls : variable_decl')
        @self.pg.production('variable_decls : variable_initialization')
        def variable_decls(p):
            print("parsing variable_decls")
            

        @self.pg.production('variable_decl : data_type IDENTIFIER decl_tail SEMI')
        def variable_decl(p):
            print("parsing variable_decl")


        @self.pg.production('decl_tail : COMMA IDENTIFIER decl_tail')
        @self.pg.production('decl_tail : ')
        def decl_tail(p):
            print("parsing decl_tail")


        @self.pg.production('variable_initialization : data_type IDENTIFIER EQUALS value initialize_tail SEMI')
        def variable_initialization(p):
            print("parsing variable_initialization")


        @self.pg.production('initialize_tail : COMMA IDENTIFIER EQUALS value initialize_tail')
        @self.pg.production('initialize_tail : ')
        def initialize_tail(p):
            print("parsing initialize_tail")

        @self.pg.production('data_type : PINCH')
        @self.pg.production('data_type : PASTA') 
        @self.pg.production('data_type : SKIM')
        @self.pg.production('data_type : BOOL')
        def data_type(p):
            print("parsing data_type")


        @self.pg.production('recipe_decl : RECIPE data_type IDENTIFIER LBRACKET PINCHLITERAL RBRACKET SEMI')
        def recipe_decl(p):
            print("parsing recipe_decl")


        @self.pg.production('recipe_init : RECIPE data_type IDENTIFIER LBRACKET PINCHLITERAL RBRACKET EQUALS LBRACE recipe_elements RBRACE SEMI')
        def recipe_init(p):
            print("parsing recipe_init")

        @self.pg.production('recipe_elements : value COMMA recipe_elements')
        @self.pg.production('recipe_elements : value')
        def recipe_elements(p):
            print("parsing recipe_elements")

        @self.pg.production('value : identifier LBRACKET expr RBRACKET')
        def value_recipe_access(p):
            print("parsing value_recipe_access")


        @self.pg.production('value : identifier')
        @self.pg.production('value : literal')
        @self.pg.production('value : expr')
        # @self.pg.production('value : pasta_concat')
        @self.pg.production('value : func_call')
        @self.pg.production('value : type_cast')
        @self.pg.production('value : esc_sequence')
        @self.pg.production('value : bool_literal')
        def value(p):
            print("parsing value")


        @self.pg.production('type_cast : data_type LPAREN value RPAREN')
        def type_cast(p):
            print("parsing type_cast")


        @self.pg.production('literal : PINCHLITERAL')
        @self.pg.production('literal : SKIMLITERAL')
        @self.pg.production('literal : NEALITERAL')
        @self.pg.production('literal : NEHLITERAL')
        @self.pg.production('literal : PASTALITERAL')
        def literal(p):
            print("parsing literal")


        @self.pg.production('identifier : IDENTIFIER')
        def identifier(p):
            print("parsing identifier")


        @self.pg.production('functions : function_definition functions')
        @self.pg.production('functions : ')
        def functions(p):
            print("parsing functions")


        @self.pg.production('function_definition : FULL data_type IDENTIFIER LPAREN parameters RPAREN LBRACE full_body RBRACE')
        @self.pg.production('function_definition : HUNGRY IDENTIFIER LPAREN parameters RPAREN LBRACE voidbody RBRACE')
        def function_definition(p):
            print("parsing function_definition")

            
        @self.pg.production('full_body : declarations stmts SPIT value SEMI')
        @self.pg.production('full_body : declarations SPIT value SEMI')
        def full_body(p):
            print("parsing full_body")

    
        @self.pg.production('func_call : IDENTIFIER LPAREN args RPAREN')
        def func_call(p):
            print("parsing func_call")

        @self.pg.production('parameters : param parameters_tail')
        @self.pg.production('parameters : ')
        def parameters(p):
            print("parsing parameters")


        @self.pg.production('parameters_tail : COMMA param parameters_tail')
        @self.pg.production('parameters_tail : ')
        def parameters_tail(p):
            print("parsing parameters_tail")


        @self.pg.production('param : data_type IDENTIFIER')
        def param(p):
            pass
    

        @self.pg.production('args : value args_tail')
        @self.pg.production('args : ')
        def args(p):
            print("parsing args")


        @self.pg.production('args_tail : COMMA value args_tail')
        @self.pg.production('args_tail : ')
        def args_tail(p):
            print("parsing args_tail")


        @self.pg.production('body : declarations stmts')
        def body(p):
            print("parsing body")


        @self.pg.production('voidbody : declarations void_stmts')
        def voidbody(p):
            print("parsing voidbody")

        @self.pg.production('void_stmts : void_stmt void_stmts')
        @self.pg.production('void_stmts : ')
        def void_stmts(p):
            print("parsing void_stmts")


        @self.pg.production('void_stmt : make_stmt SEMI')
        @self.pg.production('void_stmt : serve_stmt SEMI')
        @self.pg.production('void_stmt : void_for_stmt')
        @self.pg.production('void_stmt : void_simmer_stmt')
        @self.pg.production('void_stmt : assignment_stmt SEMI')
        @self.pg.production('void_stmt : func_call SEMI')
        @self.pg.production('void_stmt : break_stmt SEMI')
        @self.pg.production('void_stmt : continue_stmt SEMI')
        def void_stmt(p):
            print("parsing void_stmt")


        @self.pg.production('stmts : stmt stmts')
        @self.pg.production('stmts : ')
        def stmts(p):
            print("parsing stmts")


        @self.pg.production('stmt : make_stmt SEMI')
        @self.pg.production('stmt : serve_stmt SEMI')
        @self.pg.production('stmt : for_stmt')
        @self.pg.production('stmt : simmer_stmt')
        @self.pg.production('stmt : assignment_stmt SEMI')
        @self.pg.production('stmt : func_call SEMI')
        @self.pg.production('stmt : pasta_concat SEMI')
        @self.pg.production('stmt : bool_expr SEMI')
        @self.pg.production('stmt : taste_stmt')  # Add this line to allow taste_stmt as stmt
        @self.pg.production('stmt : break_stmt SEMI')
        # @self.pg.production('stmt : continue_stmt SEMI')
        def stmt(p):
            print("parsing stmt")


        @self.pg.production('break_stmt : CHOP')
        def break_stmt(p):
            print("parsing break_stmt")


        # @self.pg.production('continue_stmt : GORA')
        # def continue_stmt(p):
        #     print("parsing continue_stmt")


        @self.pg.production('next_stmts : dish_stmt next_stmts')
        @self.pg.production('next_stmts : ')
        def next_stmts(p):
            print("parsing next_stmts")


        @self.pg.production('spit_stmt : SPIT value SEMI')
        def spit_stmt(p):
            print("parsing spit_stmt")

        @self.pg.production('dish_stmt : stmt')
        @self.pg.production('dish_stmt : taste_stmt')
        def dish_stmt(p):
            print("parsing dish_stmt")

        @self.pg.production('make_stmt : MAKE LPAREN IDENTIFIER RPAREN')
        def make_stmt(p):
            print("parsing make_stmt")

        @self.pg.production('serve_stmt : SERVE LPAREN pasta_concat RPAREN')
        @self.pg.production('serve_stmt : SERVE LPAREN value RPAREN')
        def serve_stmt(p):
            print("parsing serve_stmt")

        @self.pg.production('for_stmt : FOR LPAREN PINCH IDENTIFIER EQUALS value SEMI rel_expr SEMI assignment_stmt RPAREN LBRACE stmts RBRACE')
        def for_stmt(p):
            print("parsing for_stmt")


        @self.pg.production('simmer_stmt : SIMMER LPAREN condition RPAREN LBRACE stmts RBRACE')
        def simmer_stmt(p):
            print("parsing simmer_stmt")


        @self.pg.production('assignment_stmt : IDENTIFIER LBRACKET expr RBRACKET EQUALS value')
        @self.pg.production('assignment_stmt : IDENTIFIER EQUALS value')
        @self.pg.production('assignment_stmt : IDENTIFIER PLUSEQUAL value')
        @self.pg.production('assignment_stmt : IDENTIFIER MINUSEQUAL value')
        @self.pg.production('assignment_stmt : IDENTIFIER STAREQUAL value')
        @self.pg.production('assignment_stmt : IDENTIFIER SLASHEQUAL value')
        @self.pg.production('assignment_stmt : IDENTIFIER PERCENTEQUAL value')
        @self.pg.production('assignment_stmt : IDENTIFIER COMMA identifier_list EQUALS func_call')
        def assignment_stmt(p):
            print("parsing assignment_stmt")

        @self.pg.production('identifier_list : IDENTIFIER COMMA identifier_list')
        @self.pg.production('identifier_list : IDENTIFIER')
        def identifier_list(p):
            pass

        @self.pg.production('expr : bool_expr')
        @self.pg.production('expr : term expr_tail')
        def expr(p):
            print("parsing expr")



        @self.pg.production('expr_tail : PLUS term expr_tail')
        @self.pg.production('expr_tail : MINUS term expr_tail')
        @self.pg.production('expr_tail : ')
        def expr_tail(p):
            print("parsing expr_tail")


        @self.pg.production('term : factor term_tail')
        def term(p):
            print("parsing term")


        @self.pg.production('term_tail : STAR factor term_tail')
        @self.pg.production('term_tail : SLASH factor term_tail')
        @self.pg.production('term_tail : PERCENT factor term_tail')
        @self.pg.production('term_tail : ')
        def term_tail(p):
            print("parsing term_tail")



        @self.pg.production('factor : NOT factor')
        @self.pg.production('factor : IDENTIFIER LBRACKET expr RBRACKET')
        @self.pg.production('factor : IDENTIFIER')
        @self.pg.production('factor : PINCHLITERAL')
        @self.pg.production('factor : SKIMLITERAL')
        @self.pg.production('factor : PASTALITERAL')
        @self.pg.production('factor : bool_literal')
        @self.pg.production('factor : LPAREN expr RPAREN')
        @self.pg.production('factor : data_type LPAREN factor RPAREN')
        def factor(p):
            print("parsing factor")



        @self.pg.production('taste_stmt : TASTE LPAREN condition RPAREN LBRACE stmts RBRACE mul_elif')
        def taste_stmt(p):
            print("parsing taste_stmt")

        @self.pg.production('mul_elif : elif_stmt mul_elif')
        @self.pg.production('mul_elif : mix_stmt')
        @self.pg.production('mul_elif : ')
        def mul_elif(p):
            print("parsing mul_elif")


        @self.pg.production('elif_stmt : ELIF LPAREN condition RPAREN LBRACE stmts RBRACE')
        def elif_stmt(p):
            print("parsing elif_stmt")


        @self.pg.production('mix_stmt : MIX LBRACE stmts RBRACE')
        def mix_stmt(p):
            print("parsing mix_stmt")


        @self.pg.production('condition : expr')
        def condition(p):
            print("parsing condition")


        @self.pg.production('bool_expr : rel_expr')
        @self.pg.production('bool_expr : bool_expr AND bool_expr')
        @self.pg.production('bool_expr : NOT bool_expr')
        @self.pg.production('bool_expr : bool_expr OR bool_expr')
        def bool_expr(p):
            print("parsing bool_expr")



        @self.pg.production('rel_expr : expr rel_op expr')
        def rel_expr(p):
            print("parsing rel_expr")

        # Relational operators
        @self.pg.production('rel_op : LT')
        @self.pg.production('rel_op : GT')
        @self.pg.production('rel_op : LTE')
        @self.pg.production('rel_op : GTE')
        @self.pg.production('rel_op : EQ')
        @self.pg.production('rel_op : NEQ')
        def rel_op(p):
            print("parsing rel_op")


        @self.pg.production('void_for_stmt : FOR LPAREN PINCH IDENTIFIER EQUALS value SEMI rel_expr SEMI assignment_stmt RPAREN LBRACE void_stmts RBRACE')
        def void_for_stmt(p):
            print("parsing void_for_stmt")



        @self.pg.production('void_simmer_stmt : SIMMER LPAREN rel_expr RPAREN LBRACE void_stmts RBRACE')
        def void_simmer_stmt(p):
            print("parsing void_simmer_stmt")


        @self.pg.production('pasta_concat : value TILDE pasta_concat')
        @self.pg.production('pasta_concat : value TILDE value')
        def pasta_concat(p):
            print("parsing pasta_concat")


        @self.pg.production('pasta_operand : IDENTIFIER')
        @self.pg.production('pasta_operand : PASTALITERAL')
        def pasta_operand(p):
            print("parsing pasta_operand")


        @self.pg.production('bool_literal : YUM')
        @self.pg.production('bool_literal : BLEH')
        def bool_literal(p):
            print("parsing bool_literal")


        @self.pg.production('esc_sequence : TAB')
        @self.pg.production('esc_sequence : NEWLINE')
        @self.pg.production('esc_sequence : BACKSLASH')
        @self.pg.production('esc_sequence : DOUBLE_QUOTE')
        def esc_sequence(p):
            print("parsing esc_sequence")