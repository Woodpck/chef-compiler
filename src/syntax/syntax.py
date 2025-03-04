cfg = {
    "<program>": [["dinein", "\n", "<global_dec>", "<function>", "chef", "pinch", "dish", "(", ")", "{", "<local_dec>", "<statement_block>", "spit", "0", ";", "}", "\n" "takeout"]],
	
    "<global_dec>": [["<declarations>", "<global_dec>"],
					["λ"]],
    
	"<declarations>": [["<data_type>", "id", "<dec_or_init>", ";"],
			["recipe", "<data_type2>", "id", "[", "pinchliterals", "]", "<elements>", ";"]],
 
	"<data_type>": [["pinch"],
                 	["skim"],
                 	["pasta"],
                 	["bool"]],
 
 	"<data_type2>": [["pinch"],
                 	["skim"],
                 	["pasta"]],
  
	"<dec_or_init>": [["=", "<literals>", "<next_dec_or_init>"],
                   	["<next_dec_or_init>"]],
 
	"<next_dec_or_init>": [[",", "id", "<dec_or_init>"],
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
 
	"<function_definition>": [["full", "<data_type>", "id", "(", "<parameters>", ")", "{", "<local_dec>", "<statement_block>", "spit", "<expression>", ";", "}"],
						["hungry", "id", "(", "<parameters>", ")", "{", "<local_dec>", "<statement_block>", "}", ";"]],
 
	"<parameters>": [["<data_type>", "id", "<param_tail>"],
					["λ"]],
 
	"<param_tail>": [[",","<data_type>", "id", "<param_tail>"],
                  	["λ"]],
 
    "<local_dec>": [["<local_declarations>", "<local_dec>"],
                    ["λ"]],
    
	"<local_declarations>": [["<data_type>", "id", "<dec_or_init>", ";"],
			["recipe", "<data_type2>", "id", "[", "pinchliterals", "]", "<elements>", ";"]],
 
    "<statement_block>": [["<statement>", "<statement_block>"],
                    ["λ"]],
    
    "<statement>": [["id", "<statement_id_tail>"],
                    ["<unary_op>", "id", ";"],
                    ["<conditional_statement>"],
                    ["<looping_statement>"],
                    ["serve", "(", "<value>", "<serve_tail>", ")", ";"],
                    ["make", "(", "id", ")", ";"]],
    
    "<statement_id_tail>": [["(", "<argument_list>", ")", ";"],
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
                ["id", "<value_id_tail>"]],
    
    "<value_id_tail>": [["(", "<argument_list>", ")"],
                ["[", "pinchliterals", "]"],
                ["λ"]],
    
    "<value2>": [["<literals2>"],
                ["id", "<value_id_tail>"]],
    
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
    
    "<looping_statement>": [["for", "(", "<pinch_opt>", "id", "=", "<value2>", ";", "<condition>", ";", "<inc_dec>", ")", "{", "<statement_block>", "}"],
                            ["simmer" , "(", "<condition>", ")", "{", "<statement_block>", "}"],
                            ["keepmix", "{", "<statement_block>", "}", "simmer", "(", "<condition>", ")"]],        
                
    "<pinch_opt>": [["pinch"],
                    ["λ"]],
    
    "<inc_dec>": [["id", "<unary_op>"],
                  ["<unary_op>", "id"]],
    
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
        self.stack = ["$", "<program>"]  # Start with end marker and start symbol
        self.input_tokens = tokens + [("$", "$", -1)]  # Append EOF
        self.index = 0
        self.parse_tree = ParseTreeNode("<program>")  # Initialize parse tree root
        node_stack = [self.parse_tree]  # Maintain node stack
        self.errors = []

        while self.stack:
            top = self.stack.pop()
            current_lexeme = self.input_tokens[self.index][0]
            current_token = self.input_tokens[self.index][1]  # Token type
            current_line = self.input_tokens[self.index][2]  # Line number
            parent_node = node_stack.pop() if node_stack else None

            print(f"Stack: {self.stack}, Top: {top}, Token: {current_token}")  # Debugging line

            if top == "λ":  # Handle lambda (empty production)
                continue  # Skip lambda and continue processing the stack

            if top == current_token:  # Terminal match
                self.index += 1
                if parent_node:
                    parent_node.add_child(ParseTreeNode(current_token))

            elif top in self.cfg:  # Non-terminal
                if current_token in self.parse_table.get(top, {}):
                    production = self.parse_table[top][current_token]
                    new_node = ParseTreeNode(top)
                    if parent_node:
                        parent_node.add_child(new_node)
                    if production != ["λ"]:
                        self.stack.extend(reversed(production))
                        node_stack.extend(reversed([ParseTreeNode(symbol) for symbol in production]))
                else:
                    # Check if lambda is allowed (i.e., current_token is in follow_set of top)
                    if "λ" in self.parse_table.get(top, {}) and current_token in self.follow_set[top]:
                        continue  # Skip lambda and continue

                    # 🔹 Fix: Get **only the first set** of next expected non-terminal  
                    expected_tokens = set(self.parse_table.get(top, {}).keys())

                    if current_token in expected_tokens:
                        self.syntax_error(current_line, None, expected_tokens)  # Only show expected tokens
                    else:
                        self.syntax_error(current_line, current_lexeme, expected_tokens)  # Show unexpected + expected
                    return False, self.errors

            else:
                self.syntax_error(current_line, current_lexeme, {top})
                return False, self.errors

        if self.index < len(self.input_tokens) - 1:
            remaining_token = self.input_tokens[self.index]
            self.syntax_error(remaining_token[2], remaining_token[0], {"EOF"})
            return False, self.errors

        return True, []
        print("Parse Tree:")
        print(self.parse_tree)

    def syntax_error(self, line, found, expected):
        """ Record a syntax error with correct expected tokens and line number. """
        if line == -1:  # Use last valid line number if not set
            line = self.input_tokens[self.index - 1][2] if self.index > 0 else 1

        if not self.stack:  
            # 🔹 Stack is empty → only report unexpected token
            error_message = f"Syntax Error at line {line}: Unexpected ' {found} '"
        elif found == '$':  
            # 🔹 Special case: No unexpected token, just missing expected ones
            error_message = f"Syntax Error at line {line}: Missing expected token(s): {', '.join(expected)}"
        else:
            # 🔹 Normal case: Unexpected token + expected tokens
            error_message = f"Syntax Error at line {line}: Unexpected ' {found} ' (Expected {', '.join(expected)})"

        self.errors.append(error_message)
       

# Run Parser
parser = LL1Parser(cfg, parse_table, follow_set)
tokens = [("dinein", "dinein", 1),
          ("chef", "chef", 1)
]
errors = parser.parse(tokens)
print((errors))





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