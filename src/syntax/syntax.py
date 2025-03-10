cfg = {

    "<program>": [["dinein", "<global_dec>", "<function>", "chef", "pinch", "dish", "(", ")", "{", "<local_dec>", "<statement_block>", "spit", "pinchliterals", ";", "}", "takeout"]],
	
    "<global_dec>": [["<declarations>", "<global_dec>"],
					["λ"]],
    
	"<declarations>": [["<data_type>", "identifier", "<dec_or_init>", ";"],
			["recipe", "<data_type2>", "identifier", "[", "pinchliterals", "]", "<elements>", ";"]],
 
	"<data_type>": [["pinch"],
                 	["skim"],
                 	["pasta"],
                 	["bool"]],
 
 	"<data_type2>": [["pinch"],
                 	["skim"],
                 	["pasta"]],
  
	"<dec_or_init>": [["=", "<literals>", "<next_dec_or_init>"],
                   	["<next_dec_or_init>"]],
 
	"<next_dec_or_init>": [[",", "identifier", "<dec_or_init>"],
                        ["λ"]],
 
	"<literals>": [["pinchliterals"],
                	["skimliterals"],
                 	["pastaliterals"],
                 	["<yum_or_bleh>"]],
 
	"<literals2>": [["pinchliterals"],
                	["skimliterals"],
                 	["pastaliterals"]],
 
	"<yum_or_bleh>": [["yum"],
                   	["bleh"]],
 
	"<elements>": [["=", "{", "<literals>", "<elementtail>", "}"],
               	["λ"]],
 
    "<elementtail>": [[",", "<literals>", "<elementtail>"],
                ["λ"]],
    
	"<function>": [["<function_definition>", "<function>"],
				["λ"]],
 
	"<function_definition>": [["full", "<data_type>", "identifier", "(", "<parameters>", ")", "{", "<local_dec>", "<statement_block>", "spit", "<expression>", ";", "}"],
						["hungry", "identifier", "(", "<parameters>", ")", "{", "<local_dec>", "<statement_block>", "}", ";"]],
 
	"<parameters>": [["<data_type>", "identifier", "<param_tail>"],
					["λ"]],
 
	"<param_tail>": [[",","<data_type>", "identifier", "<param_tail>"],
                  	["λ"]],
 
    "<local_dec>": [["<local_declarations>", "<local_dec>"],
                    ["λ"]],
    
	"<local_declarations>": [["<data_type>", "identifier", "<dec_or_init>", ";"],
			["recipe", "<data_type2>", "identifier", "[", "pinchliterals", "]", "<elements>", ";"]],
 
    "<statement_block>": [["<statement>", "<statement_block>"],
                    ["λ"]],
    
    "<statement>": [["identifier", "<statement_identifier_tail>"],
                    ["<unary_op>", "identifier", ";"],
                    ["<conditional_statement>"],
                    ["<looping_statement>"],
                    ["serve", "(", "<value>", "<serve_tail>", ")", ";"],
                    ["make", "(", "identifier", ")", ";"]],
    
    "<statement_identifier_tail>": [["(", "<argument_list>", ")", ";"],
                            ["<assignment_op>", "<expression>", ";"],
                            ["[", "pinchliterals", "]", "<assignment_op>", "<arithmetic_exp>", ";"],
                            ["<unary_op>", ";"]],
    
    "<argument_list>": [["<arithmetic_exp>", "<argument_tail>"],
                        ["λ"]],
    
    "<argument_tail>": [[",", "<arithmetic_exp>" , "<argument_tail>"],
                        ["λ"]],
    
    "<expression>": [["<expression_operand>", "<expression_tail>"]],
    
    "<expression_tail>": [["<expression_operator>", "<expression_operand>", "<expression_tail>"],
                        ["λ"]],
    
    "<expression_operand>": [["<value>"],
                             ["(", "<expression>", ")"],
                             ["!", "(", "<expression>", ")"],
                             ["!!", "(", "<expression>", ")"]],
    
    "<expression_operator>": [["+"],
                            ["-"],
                            ["*"],
                            ["/"],
                            ["%"],
                            ["=="],
                            ["!="],
                            ["<"],
                            [">"],
                            ["<="],
                            [">="],
                            ["&&"],
				            ["??"]],
    
    "<arithmetic_exp>": [["<arithmetic_operand>", "<arithmetic_tail>"]],
    
    "<arithmetic_tail>": [["<arithmetic_operator>", "<arithmetic_operand>", "<arithmetic_tail>"],
                          ["λ"]],
    
    "<arithmetic_operand>": [["<value2>"],
                             ["(", "<arithmetic_exp>", ")"]],
    
    "<arithmetic_operator>": [["+"],
                            ["-"],
                            ["*"],
                            ["/"],
                            ["%"]],
    
    "<value>": [["<literals>"],
                ["identifier", "<value_identifier_tail>"]],
    
    "<value_identifier_tail>": [["(", "<argument_list>", ")"],
                ["[", "pinchliterals", "]"],
                ["λ"]],
    
    "<value2>": [["<literals2>"],
                ["identifier", "<value_identifier_tail>"]],
    
	"<assignment_op>": [["="],
				["+="],
				["-="],
				["*="],
				["/="],
				["%="]],
 
    "<unary_op>": [["++"],
                   ["--"]],
    
    "<conditional_statement>": [["taste", "(", "<condition>", ")", "{", "<statement_block>", "}", "<conditional_tail>"],
                                ["flip", "(", "<expression>", ")", "{", "case", "<literals>", ":", "<statement_block>", "chop", ";", "<case_tail>", "<default_block>", "}"]],
    
    "<conditional_tail>": [["elif", "(", "<condition>", ")", "{", "<statement_block>", "}", "<conditional_tail>"],
                            ["mix", "{", "<statement_block>", "}"],
                            ["λ"]],
    
    "<condition>": [["<condition_operand>", "<condition_tail>"]],
    
    "<condition_tail>": [["<condition_operator>", "<condition_operand>", "<condition_tail>"],
                        ["λ"]],
    
    "<condition_operand>": [["<value>"],
                            ["(", "<condition>", ")"],
                            ["!", "(", "<condition>", ")"],
                            ["!!", "(", "<condition>", ")"]],
    
    "<condition_operator>": [["=="],
                             ["!="],
                             ["<"],
                             [">"],
                             ["<="],
                             [">="],
                             ["&&"],
                             ["??"]],
    
    "<case_tail>": [["case", "<literals>", ":", "<statement_block>", "chop", ";", "<case_tail>"],
                       ["λ"]],
    
    "<default_block>": [["default", ":", "<statement_block>", "chop", ";"],
                       ["λ"]],
    
    "<looping_statement>": [["for", "(", "<pinch_opt>", "identifier", "=", "<value2>", ";", "<condition>", ";", "<inc_dec>", ")", "{", "<statement_block>", "}"],
                            ["simmer" , "(", "<condition>", ")", "{", "<statement_block>", "}"],
                            ["keepmix", "{", "<statement_block>", "}", "simmer", "(", "<condition>", ")"]],        
                
    "<pinch_opt>": [["pinch"],
                    ["λ"]],
    
    "<inc_dec>": [["identifier", "<unary_op>"],
                  ["<unary_op>", "identifier"]],
    
    "<serve_tail>": [["+", "<value>", "<serve_tail>"],
                     ["λ"]]
}

def compute_first_set(cfg):
    first_set = {non_terminal: set() for non_terminal in cfg.keys()}

    def first_of(symbol):
        if symbol not in cfg:
            return {symbol} 

        if symbol in first_set and first_set[symbol]:
            return first_set[symbol]

        result = set()
        
        for production in cfg[symbol]:
            for sub_symbol in production:
                if sub_symbol not in cfg: # terminal
                    result.add(sub_symbol)
                    break  
                else: # non-terminal
                    sub_first = first_of(sub_symbol)
                    result.update(sub_first - {"λ"})  
                    if "λ" not in sub_first:
                        break  
            
            else: # all symbols in the production derive λ
                result.add("λ")

        first_set[symbol] = result
        return result

    for non_terminal in cfg:
        first_of(non_terminal)

    return first_set

def compute_follow_set(cfg, start_symbol, first_set):
    follow_set = {non_terminal: set() for non_terminal in cfg.keys()}
    follow_set[start_symbol].add("$")  

    changed = True  

    while changed:
        changed = False 
    
        for non_terminal, productions in cfg.items():
            for production in productions:
                for i, item in enumerate(production):
                    if item in cfg:  # nt only
                        follow_before = follow_set[item].copy()

                        if i + 1 < len(production):  # A -> <alpha>B<beta>
                            beta = production[i + 1]
                            if beta in cfg:  # if <beta> is a non-terminal
                                follow_set[item].update(first_set[beta] - {"λ"})
                                if "λ" in first_set[beta]:
                                    follow_set[item].update(follow_set[beta])
                            else:  # if <beta> is a terminal
                                follow_set[item].add(beta)
                        else:  # nothing follows B
                            follow_set[item].update(follow_set[non_terminal])

                        if follow_set[item] != follow_before:
                            changed = True  

    return follow_set

def compute_predict_set(cfg, first_set, follow_set):
    predict_set = {}  

    for non_terminal, productions in cfg.items():
        for production in productions:
            production_key = (non_terminal, tuple(production))  # A = (A,(prod))
            predict_set[production_key] = set()

            first_alpha = set()
            for symbol in production:
                if symbol in first_set:  # non-terminal
                    first_alpha.update(first_set[symbol] - {"λ"})
                    if "λ" not in first_set[symbol]:
                        break
                else:  # terminal
                    first_alpha.add(symbol)
                    break
            else:  
                first_alpha.add("λ")

            predict_set[production_key].update(first_alpha - {"λ"})

            # if λ in first_alpha, add follow set of lhs to predict set
            if "λ" in first_alpha:
                predict_set[production_key].update(follow_set[non_terminal])

    return predict_set

def gen_parse_table():
    parse_table = {}
    for (non_terminal, production), predict in predict_set.items():
        if non_terminal not in parse_table:
            parse_table[non_terminal] = {}
        for terminal in predict:
            if terminal in parse_table[non_terminal]:
                raise ValueError(f"Grammar is not LL(1): Conflict in parse table for {non_terminal} and {terminal}")
            parse_table[non_terminal][terminal] = production

    return parse_table  

first_set = compute_first_set(cfg)
follow_set = compute_follow_set(cfg, "<program>", first_set)
predict_set = compute_predict_set(cfg, first_set, follow_set)
parse_table = gen_parse_table()

class ParseTreeNode:
    def __init__(self, value):
        self.value = value
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def __repr__(self, level=0):
        ret = "  " * level + repr(self.value) + "\n"
        for child in self.children:
            ret += child.__repr__(level + 1)
        return ret

class LL1Parser:
    def __init__(self, cfg, parse_table, follow_set):
        self.cfg = cfg
        self.parse_table = parse_table
        self.follow_set = follow_set
        self.stack = []
        self.input_tokens = []
        self.index = 0
        self.parse_tree = None
        self.errors = []

    def parse(self, tokens):
        # Robust token processing that normalizes identifiers but preserves lexemes
        def safe_process_token(token):
            try:
                if isinstance(token, tuple):
                    lexeme = token[0]
                    token_type = token[1]
                    line = token[2] if len(token) > 2 else -1
                    
                    # Only normalize the token type for identifiers, preserve the lexeme
                    if isinstance(token_type, str) and token_type.startswith("identifier"):
                        normalized_token = (lexeme, "identifier", line)
                    else:
                        normalized_token = (lexeme, token_type, line)
                    
                    return normalized_token
                else:
                    return (str(token), str(token), -1)
            except Exception as e:
                print(f"Error processing token {token}: {e}")
                return (str(token), str(token), -1)

        # Safely preprocess tokens
        try:
            processed_tokens = [safe_process_token(token) for token in tokens]
            processed_tokens.append(('$', '$', -1))  # Add end marker
            
            # Debug: Print processed tokens after normalization
            print("DEBUG: Received Tokens (after normalization):")
            for i, token in enumerate(processed_tokens[:-1]):  # Skip the $ token in debug output
                print(f"Token {i}: {token}")
                
        except Exception as e:
            print(f"ERROR during token processing: {e}")
            return False, [f"Token processing error: {e}"]

        # Check if processed tokens are empty
        if not processed_tokens:
            print("ERROR: No tokens were processed!")
            return False, ["No tokens found for parsing"]
        
        # Initialize parsing
        self.input_tokens = processed_tokens
        self.index = 0
        self.stack = ['$', '<program>']  # Start with end marker and start symbol
        self.parse_tree = ParseTreeNode('<program>')  # Root of parse tree
        current_node = self.parse_tree

        while self.stack[-1] != '$':
            top = self.stack[-1]
            current_token = self.input_tokens[self.index][1]
            
            # Debugging print
            print(f"DEBUG: Stack: {self.stack}, Current Token: {current_token}")

            if top not in self.cfg:  # Terminal
                if top == current_token:
                    self.stack.pop()
                    self.index += 1
                    # Pop the last child node for terminal matching
                    if current_node.children and current_node.children[-1].value == top:
                        current_node = current_node.children[-2] if len(current_node.children) > 1 else self.parse_tree
                else:
                    # Syntax error: unexpected token
                    expected = [t for t in self.parse_table.get(self.stack[-2], {}).keys()]
                    self.syntax_error(self.input_tokens[self.index][2], current_token, expected)
                    return False, self.errors
            else:  # Non-terminal
                try:
                    production = self.parse_table[top].get(current_token)
                    if production is None:
                        # No production found
                        expected = list(self.parse_table[top].keys())
                        self.syntax_error(self.input_tokens[self.index][2], current_token, expected)
                        return False, self.errors

                    # Pop the top of the stack
                    self.stack.pop()

                    # Handle lambda (empty) production
                    if production[0] != 'λ':
                        # Push production symbols in reverse order
                        for symbol in reversed(production):
                            self.stack.append(symbol)

                        # Build parse tree
                        node = ParseTreeNode(top)
                        for symbol in production:
                            child = ParseTreeNode(symbol)
                            node.add_child(child)
                        current_node.children.append(node)
                        current_node = node
                except KeyError:
                    # No production for this non-terminal and token
                    expected = list(self.parse_table.get(top, {}).keys())
                    self.syntax_error(self.input_tokens[self.index][2], current_token, expected)
                    return False, self.errors

        # Successful parse
        if self.index == len(self.input_tokens) - 1:
            print("Parsing successful!")
            return True, []
        else:
            # Incomplete parsing
            print("Parsing did not consume all tokens!")
            return False, ["Incomplete parsing"]

    def syntax_error(self, line, found, expected):
        """ Record a syntax error with correct expected tokens and line number. """
        if line == -1:  # Use last valid line number if not set
            line = self.input_tokens[self.index - 1][2] if self.index > 0 else 1

        if not self.stack:  
            # Stack is empty → only report unexpected token
            error_message = f"Syntax Error at line {line}: Unexpected ' {found} '"
        elif found == '$':  
            # Special case: No unexpected token, just missing expected ones
            error_message = f"Syntax Error at line {line}: Missing expected token(s): {', '.join(expected)}"
        else:
            # Normal case: Unexpected token + expected tokens
            error_message = f"Syntax Error at line {line}: Unexpected ' {found} ' (Expected {', '.join(expected)})"

        self.errors.append(error_message)


# for non_terminal, productions in cfg.items():
#     for i, item in enumerate(productions):
#         print(f"{non_terminal} -> {productions[i]}")

# print("First Sets:")
# for non_terminal, first in first_set.items():
#     print(f"First({non_terminal})")

# print("\nFollow Sets:")
# for non_terminal, follow in follow_set.items():
#     print(f"Follow({non_terminal})")

# def display_predict_sets(predict_set):
#     print("\nPredict Sets:")
#     for (non_terminal, production), predict in predict_set.items():
#         production_str = ", ".join(production)
#         print(f"{predict}")

# display_predict_sets(predict_set)

# def display_parse_table(parse_table):
#     print()
#     for non_terminal, rules in parse_table.items():
#         print(f"Non-terminal: {non_terminal}")
#         for terminal, production in rules.items():
#             print(f"  Terminal: {terminal} -> Production: {production}")
#         print()  

# display_parse_table(parse_table)

def check_ambiguity(cfg, predict_set):
    ambiguous_productions = []

    for non_terminal, productions in cfg.items():
        prediction_sets = [predict_set[(non_terminal, tuple(prod))] for prod in productions]
        for i in range(len(prediction_sets)):
            for j in range(i + 1, len(prediction_sets)):
                if prediction_sets[i].intersection(prediction_sets[j]):
                    ambiguous_productions.append((non_terminal, productions[i], productions[j]))

    if ambiguous_productions:
        print("\nAmbiguities found in the CFG:")
        for non_terminal, prod1, prod2 in ambiguous_productions:
            print(f"  {non_terminal} -> {prod1} | {prod2}")
    else:
        print("\nNo ambiguities found in the CFG.")

check_ambiguity(cfg, predict_set)


# for non_terminal, productions in cfg.items():
#     for i, item in enumerate(productions):
#         print(f"{non_terminal} -> {productions[i]}")

# print("First Sets:")
# for non_terminal, first in first_set.items():
#     print(f"First({non_terminal})")

# print("\nFollow Sets:")
# for non_terminal, follow in follow_set.items():
#     print(f"Follow({non_terminal})")

# def display_predict_sets(predict_set):
#     print("\nPredict Sets:")
#     for (non_terminal, production), predict in predict_set.items():
#         production_str = ", ".join(production)
#         print(f"{predict}")

# display_predict_sets(predict_set)

# def display_parse_table(parse_table):
#     print()
#     for non_terminal, rules in parse_table.items():
#         print(f"Non-terminal: {non_terminal}")
#         for terminal, production in rules.items():
#             print(f"  Terminal: {terminal} -> Production: {production}")
#         print()  

# display_parse_table(parse_table)

def check_ambiguity(cfg, predict_set):
    ambiguous_productions = []

    for non_terminal, productions in cfg.items():
        prediction_sets = [predict_set[(non_terminal, tuple(prod))] for prod in productions]
        for i in range(len(prediction_sets)):
            for j in range(i + 1, len(prediction_sets)):
                if prediction_sets[i].intersection(prediction_sets[j]):
                    ambiguous_productions.append((non_terminal, productions[i], productions[j]))

    if ambiguous_productions:
        print("\nAmbiguities found in the CFG:")
        for non_terminal, prod1, prod2 in ambiguous_productions:
            print(f"  {non_terminal} -> {prod1} | {prod2}")
    else:
        print("\nNo ambiguities found in the CFG.")

check_ambiguity(cfg, predict_set)