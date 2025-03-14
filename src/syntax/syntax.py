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
						["hungry", "identifier", "(", "<parameters>", ")", "{", "<local_dec>", "<statement_block>", "}"]],
 
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
    def __init__(self, token_value):
        # If the token is in the format "token_type:literal", store only the literal.
        if isinstance(token_value, str) and ':' in token_value:
            # Split on the first colon and take the second part.
            self.value = token_value.split(':', 1)[1]
        else:
            self.value = token_value
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def __str__(self, level=0):
        ret = "  " * level + repr(self.value) + "\n"
        for child in self.children:
            ret += child.__str__(level + 1)
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
                    # Ensure we have at least lexeme, token_type, and line_number
                    if len(token) >= 3:
                        lexeme = token[0]
                        token_type = token[1]
                        line_number = token[2]  # This should be the actual line number from the source
                    else:
                        # If token doesn't have all required elements, try to extract what we can
                        lexeme = token[0] if len(token) > 0 else ""
                        token_type = token[1] if len(token) > 1 else str(lexeme)
                        line_number = -1  # Missing line number
                    
                    # Only normalize the token type for identifiers, preserve the lexeme
                    if isinstance(token_type, str) and token_type.startswith("identifier"):
                        normalized_token = (lexeme, "identifier", line_number)
                    else:
                        normalized_token = (lexeme, token_type, line_number)
                    
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
                print(f"Token {i}: Lexeme={token[0]}, Type={token[1]}, Line={token[2]}")
                
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
        node_stack = [current_node]  # Stack to keep track of parent nodes

        while self.stack[-1] != '$':
            top = self.stack[-1]
            current_token = self.input_tokens[self.index][1]
            current_line = self.input_tokens[self.index][2]  # Get source line number
            
            # Debugging print
            print(f"DEBUG: Stack: {self.stack}, Current Token: {current_token}, Line: {current_line}, Current Node: {current_node.value}")

            if top not in self.cfg:  # Terminal
                if top == current_token:
                    self.stack.pop()
                    # Add terminal node to parse tree with lexeme
                    terminal_node = ParseTreeNode(f"{top}:{self.input_tokens[self.index][0]}")
                    current_node.add_child(terminal_node)
                    self.index += 1
                else:
                    # Syntax error: unexpected token
                    expected = [t for t in self.parse_table.get(self.stack[-2], {}).keys()]
                    self.syntax_error(current_line, current_token, expected)
                    return False, self.errors
            else:  # Non-terminal
                try:
                    production = self.parse_table[top].get(current_token)
                    if production is None:
                        # No production found
                        expected = list(self.parse_table[top].keys())
                        self.syntax_error(current_line, current_token, expected)
                        return False, self.errors

                    # Pop the top of the stack
                    self.stack.pop()
                    
                    # Create node for this non-terminal
                    non_terminal_node = ParseTreeNode(top)
                    current_node.add_child(non_terminal_node)

                    # Handle lambda (empty) production
                    if production[0] == 'λ':
                        # Add lambda node explicitly
                        lambda_node = ParseTreeNode('λ')
                        non_terminal_node.add_child(lambda_node)
                    else:
                        # Push production symbols in reverse order
                        for symbol in reversed(production):
                            self.stack.append(symbol)
                        
                        # Update current node for children
                        node_stack.append(current_node)
                        current_node = non_terminal_node
                except KeyError:
                    # No production for this non-terminal and token
                    expected = list(self.parse_table.get(top, {}).keys())
                    self.syntax_error(current_line, current_token, expected)
                    return False, self.errors
            
            # Check if we need to move back up the tree
            while (len(self.stack) >= 2 and 
                   self.stack[-1] not in self.cfg and 
                   current_node != self.parse_tree and 
                   len(node_stack) > 0):
                next_symbol = self.stack[-1]
                if next_symbol in self.cfg:  # If next symbol is non-terminal, don't pop yet
                    break
                current_node = node_stack.pop()

        # Successful parse
        if self.index == len(self.input_tokens) - 1:
            print("Parsing successful!")
            # Print parse tree for debugging
            print("PARSE TREE:")
            print(self.parse_tree)
            return True, []
        else:
            # Incomplete parsing
            print("Parsing did not consume all tokens!")
            return False, ["Incomplete parsing"]

    def syntax_error(self, line_number, found, expected):
        """Record a syntax error with detailed information about the error location and expected tokens."""
        # Get the actual lexeme for better error messages
        token_lexeme = self.input_tokens[self.index][0] if self.index < len(self.input_tokens) else found
        
        # Filter out redundant or irrelevant expected tokens
        filtered_expected = []
        if expected:
            # Remove duplicates and sort for consistent error messages
            filtered_expected = sorted(set(expected))
            # Remove lambda if it's in the expected list for clearer error messages
            if "λ" in filtered_expected:
                filtered_expected.remove("λ")
        
        # Ensure we have a valid line number
        if line_number == -1 or line_number is None:
            line_number = "unknown"
        
        # Handle different error scenarios
        if not self.stack:
            # Stack is empty, but we still have tokens → unexpected extra tokens
            error_message = f"Syntax Error at line {line_number}: Unexpected token '{token_lexeme}' after parsing completed"
        elif found == '$' and self.stack[-1] != '$':
            # Unexpected end of input - something is missing
            top_symbol = self.stack[-1]
            missing_desc = f"'{top_symbol}'" if top_symbol not in self.cfg else "required tokens"
            error_message = f"Syntax Error at line {line_number}: Unexpected end of input, missing {missing_desc}"
        elif filtered_expected:
            # We have expected tokens to report
            expected_str = ", ".join(f"'{e}'" for e in filtered_expected)
            error_message = f"Syntax Error at line {line_number}: Unexpected '{token_lexeme}', expected {expected_str}"
        else:
            # No specific expected tokens to report
            error_message = f"Syntax Error at line {line_number}: Unexpected '{token_lexeme}'"
        
        # Add context about current parsing state
        current_context = None
        try:
            # Try to get the non-terminal we're currently parsing for context
            for i in range(len(self.stack) - 1, -1, -1):
                if self.stack[i] in self.cfg:
                    current_context = self.stack[i]
                    break
            
            if current_context:
                error_message += f" while parsing <{current_context}>"
        except Exception:
            # If determining context fails, just continue without it
            pass
        
        # Add a recovery hint if possible
        if filtered_expected and len(filtered_expected) <= 3:
            error_message += f" - consider adding {' or '.join(f"'{e}'" for e in filtered_expected)}"
        
        self.errors.append(error_message)
        
        # Debug info can be helpful when troubleshooting
        debug_info = f"DEBUG: Stack: {self.stack}, Current index: {self.index}, Line number: {line_number}"
        print(debug_info)
        
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