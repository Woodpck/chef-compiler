class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}
        self.function_table = {}
        self.arrays = {}
        self.current_scope = "global"
        self.scopes = ["global"]
        self.errors = []
        self.current_function = None
        self.output_messages = []

    def analyze(self, parse_tree):
        if not parse_tree:
            error_msg = "No parse tree available for semantic analysis"
            self.errors.append(error_msg)
            self.output_messages.append(error_msg)
            return False, self.errors  # Return errors, not output_messages when failed

        print("Starting semantic analysis...")
        print(f"Parse Tree Root: {parse_tree.value}")
        self.output_messages.append("Starting semantic analysis...")

        # Start the analysis with the root flag set to True.
        self._analyze_node(parse_tree, is_root=True)

        for func_name, func_info in self.function_table.items():
            if func_info["return_type"] != "hungry" and not func_info.get("has_return", False):
                error_msg = f"Semantic Error: Function '{func_name}' must return a value of type {func_info['return_type']}"
                self.errors.append(error_msg)
                self.output_messages.append(error_msg)

        if self.errors:
            print(f"Semantic analysis found {len(self.errors)} errors")
            return False, self.errors  # Return errors when failed

        self.output_messages.append("Semantic analysis completed successfully!")
        return True, self.output_messages

    def _analyze_node(self, node, is_root=False):
        if not node or not hasattr(node, "value"):
            return

        # Process the current node based on its type
        if node.value == "<program>":
            if is_root:
                self._analyze_program(node)
                # Print a debug message to track progress
                self.output_messages.append("Processed program node")
        elif node.value == "<global_dec>":
            self._analyze_global_declarations(node)
            self.output_messages.append("Processed global declarations")
        elif node.value == "<function>":
            self._analyze_functions(node)
            self.output_messages.append("Processed function")
        elif node.value == "<function_definition>":
            self._analyze_function_definition(node)
            self.output_messages.append("Processed function definition")
        elif node.value == "<local_dec>":
            self._analyze_local_declarations(node)
            self.output_messages.append("Processed local declarations")
        elif node.value == "<statement_block>":
            self._analyze_statements(node)
            self.output_messages.append("Processed statements")

        # Add debug output before traversing children
        if node.children:
            self.output_messages.append(f"Traversing {len(node.children)} children of {node.value}")
        
        # Traverse children
        for child in node.children:
            self._analyze_node(child, is_root=False)

    def _analyze_program(self, node):
        # Check that the very first and very last token children are 'dinein' and 'takeout'.
        # Filter out non-token nodes (assuming tokens do not start with '<')
        token_children = [child for child in node.children if not (isinstance(child.value, str) and child.value.startswith("<"))]
        
        if not token_children or token_children[0].value != "dinein":
            self.errors.append("Semantic Error: Missing 'dinein' at the beginning of the program")
        if not token_children or token_children[-1].value != "takeout":
            self.errors.append("Semantic Error: Missing 'takeout' at the end of the program")

    def _analyze_global_declarations(self, node):
        """Analyze global variable declarations"""
        for child in node.children:
            if child.value == "<declarations>":
                self._analyze_declaration(child, "global")

    def _analyze_local_declarations(self, node):
        """Analyze local variable declarations"""
        for child in node.children:
            if child.value == "<local_declarations>":
                self._analyze_declaration(child, self.current_scope)

    def _analyze_declaration(self, node, scope):
        """Analyze a variable declaration"""
        # Extract data type, identifier, and initialization
        data_type = None
        identifier = None
        initialization = None
        line = -1  # Default line number if not available
        
        print(f"DEBUG: Analyzing declaration node: {node.value} with {len(node.children)} children")
        print(f"DEBUG: Children values: {[child.value for child in node.children]}")
        
        # Extract data type
        for child in node.children:
            print(f"DEBUG: Checking child: {child.value}")
            if child.value == "<data_type>":
                data_type = self._extract_data_type(child)
                print(f"DEBUG: Found data type: {data_type}")
            elif child.value == "identifier":
                # Extract the actual identifier lexeme and line number
                if hasattr(child, "lexeme"):
                    identifier = child.lexeme
                    line = child.line
                elif child.children and hasattr(child.children[0], "lexeme"):
                    identifier = child.children[0].lexeme
                    line = child.children[0].line
                print(f"DEBUG: Found identifier: {identifier} at line {line}")
            elif child.value == "<dec_or_init>":
                # Variable initialization
                print(f"DEBUG: Found dec_or_init, extracting initialization")
                initialization = self._extract_initialization(child)
                print(f"DEBUG: Initialization result: {initialization}")
        
        if identifier is None:
            print("DEBUG: No identifier found, returning early")
            return  # Can't process without an identifier
        
        # Check if variable is already declared in the current scope
        symbol_key = f"{scope}.{identifier}"
        if symbol_key in self.symbol_table:
            error_msg = f"Semantic Error at line {line}: Variable '{identifier}' already declared in this scope"
            print(f"DEBUG: Adding error: {error_msg}")
            self.errors.append(error_msg)
            return
        
        # Process regular variable declaration
        if data_type is None:
            error_msg = f"Semantic Error at line {line}: Variable '{identifier}' declared without a valid data type"
            print(f"DEBUG: Adding error: {error_msg}")
            self.errors.append(error_msg)
            return
        
        # Store variable info
        self.symbol_table[symbol_key] = {
            "type": data_type,
            "initialized": initialization is not None,
            "line": line,
            "scope": scope
        }
        print(f"DEBUG: Added to symbol table: {symbol_key} = {self.symbol_table[symbol_key]}")
        
        # Check initialization type compatibility
        if initialization is not None:
            init_type = initialization["type"]
            print(f"DEBUG: Checking type compatibility: {init_type} vs {data_type}")
            if not self._is_compatible_type(init_type, data_type):
                error_msg = f"Semantic Error at line {line}: Type mismatch in initialization of '{identifier}': expected {data_type}, got {init_type}"
                print(f"DEBUG: Adding error: {error_msg}")
                self.errors.append(error_msg)
                self.output_messages.append(error_msg)  # Add to output messages as well

    def _extract_data_type(self, node):
        """Extract data type from a <data_type> node"""
        for child in node.children:
            if child.value in ["pinch", "skim", "pasta", "bool"]:
                return child.value
        return None

    def _extract_initialization(self, node):
        """Extract initialization value and type from <dec_or_init> node"""
        print(f"DEBUG: Extracting initialization from {node.value} with {len(node.children)} children")
        print(f"DEBUG: Children: {[child.value for child in node.children]}")
        
        for child in node.children:
            if child.value == "=":
                print("DEBUG: Found assignment operator '='")
                # First, try to find a direct expression
                for sibling in node.children:
                    print(f"DEBUG: Checking sibling for literals: {sibling.value}")
                    if sibling.value == "<expression>":
                        print("DEBUG: Found expression node")
                        for expr_child in sibling.children:
                            print(f"DEBUG: Expression child: {expr_child.value}")
                            if expr_child.value == "<literals>":
                                print("DEBUG: Found literals node in expression")
                                result = self._extract_literal_value(expr_child)
                                print(f"DEBUG: Extracted literal value: {result}")
                                return result
                            # Check if the expression child is a string literal
                            if isinstance(expr_child.value, str) and expr_child.value.startswith('"') and expr_child.value.endswith('"'):
                                print(f"DEBUG: Found string literal: {expr_child.value}")
                                return {"value": expr_child.value.strip('"'), "type": "pasta"}
                    
                    # Check if this sibling is a string literal
                    if isinstance(sibling.value, str) and sibling.value.startswith('"') and sibling.value.endswith('"'):
                        print(f"DEBUG: Found direct string literal: {sibling.value}")
                        return {"value": sibling.value.strip('"'), "type": "pasta"}
                    
                    # Check if the sibling has a <literals> child
                    if hasattr(sibling, 'children'):
                        for s_child in sibling.children:
                            print(f"DEBUG: Checking sibling's child: {s_child.value}")
                            if s_child.value == "<literals>":
                                print("DEBUG: Found literals node in sibling")
                                result = self._extract_literal_value(s_child)
                                print(f"DEBUG: Extracted literal value: {result}")
                                return result
                            
                            # Check if this is a string literal
                            if isinstance(s_child.value, str) and s_child.value.startswith('"') and s_child.value.endswith('"'):
                                print(f"DEBUG: Found string literal in sibling: {s_child.value}")
                                return {"value": s_child.value.strip('"'), "type": "pasta"}
                
                print("DEBUG: No literals found after exhaustive search")
        
        print("DEBUG: No initialization value found")
        return None

    def _extract_array_elements(self, node):
        """Extract array elements from <elements> node"""
        elements = []
        for child in node.children:
            if child.value == "<literals>":
                element = self._extract_literal_value(child)
                if element:
                    elements.append(element)
            elif child.value == "<elementtail>":
                # Process additional elements
                more_elements = self._extract_elementtail(child)
                if more_elements:
                    elements.extend(more_elements)
        return elements

    def _extract_elementtail(self, node):
        """Extract elements from <elementtail> node"""
        elements = []
        for child in node.children:
            if child.value == "<literals>":
                element = self._extract_literal_value(child)
                if element:
                    elements.append(element)
            elif child.value == "<elementtail>":
                # Recursive processing for nested tails
                more_elements = self._extract_elementtail(child)
                if more_elements:
                    elements.extend(more_elements)
        return elements

    def _extract_literal_value(self, node):
        """Extract literal value and its type"""
        print(f"DEBUG: Extracting literal value from {node.value} with {len(node.children)} children")
        print(f"DEBUG: Children: {[child.value for child in node.children]}")
        
        for child in node.children:
            print(f"DEBUG: Checking literal child: {child.value}")
            # Check for specific literal tokens
            if child.value in ["pinchliterals", "skimliterals", "pastaliterals"]:
                print(f"DEBUG: Found typed literal: {child.value}")
                value = None
                if hasattr(child, "lexeme"):
                    value = child.lexeme
                    print(f"DEBUG: Literal lexeme: {value}")
                elif child.children and hasattr(child.children[0], "lexeme"):
                    value = child.children[0].lexeme
                    print(f"DEBUG: Literal child lexeme: {value}")
                
                type_map = {
                    "pinchliterals": "pinch",
                    "skimliterals": "skim",
                    "pastaliterals": "pasta"
                }
                result = {"value": value, "type": type_map[child.value]}
                print(f"DEBUG: Returning literal result: {result}")
                return result
                
            # Check for string literal tokens
            elif isinstance(child.value, str) and child.value.startswith('"') and child.value.endswith('"'):
                print(f"DEBUG: Found string literal: {child.value}")
                value = child.value.strip('"')
                result = {"value": value, "type": "pasta"}
                print(f"DEBUG: Returning string result: {result}")
                return result
        
        print("DEBUG: No literal value found")
        return None

    def _analyze_functions(self, node):
        """Analyze function declarations"""
        for child in node.children:
            if child.value == "<function_definition>":
                self._analyze_function_definition(child)

    def _analyze_function_definition(self, node):
        """Analyze a function definition"""
        # Extract function information
        return_type = None
        identifier = None
        parameters = []
        is_void = False
        line = -1
        
        # Check if it's a void (hungry) function
        for child in node.children:
            if child.value == "hungry":
                is_void = True
                break
        
        for child in node.children:
            if child.value == "<data_type>":
                return_type = self._extract_data_type(child)
            elif child.value == "identifier":
                # Extract function name
                if hasattr(child, "lexeme"):
                    identifier = child.lexeme
                    line = child.line
                elif child.children and hasattr(child.children[0], "lexeme"):
                    identifier = child.children[0].lexeme
                    line = child.children[0].line
            elif child.value == "<parameters>":
                parameters = self._extract_parameters(child)
        
        if identifier is None:
            return  # Can't process without a function name
        
        # Set return type for void functions
        if is_void:
            return_type = "hungry"
        
        # Check if function is already declared
        if identifier in self.function_table:
            self.errors.append(f"Semantic Error at line {line}: Function '{identifier}' already declared")
            return
        
        # Store function info
        self.function_table[identifier] = {
            "return_type": return_type,
            "params": parameters,
            "line": line,
            "has_return": False  # Will be set to True when a return statement is found
        }
        
        # Set current function and scope for analysis of the function body
        self.current_function = identifier
        self.current_scope = identifier
        self.scopes.append(identifier)
        
        # Add parameters to symbol table in function scope
        for param_type, param_name in parameters:
            symbol_key = f"{identifier}.{param_name}"
            self.symbol_table[symbol_key] = {
                "type": param_type,
                "initialized": True,  # Parameters are always initialized
                "line": line,
                "scope": identifier
            }
    
    def _extract_parameters(self, node):
        """Extract function parameters"""
        parameters = []
        
        data_type = None
        param_name = None
        
        for child in node.children:
            if child.value == "<data_type>":
                data_type = self._extract_data_type(child)
            elif child.value == "identifier":
                # Extract parameter name
                if hasattr(child, "lexeme"):
                    param_name = child.lexeme
                elif child.children and hasattr(child.children[0], "lexeme"):
                    param_name = child.children[0].lexeme
                
                if data_type and param_name:
                    parameters.append((data_type, param_name))
                    data_type = None
                    param_name = None
            
            elif child.value == "<param_tail>":
                # Process additional parameters
                more_params = self._extract_param_tail(child)
                if more_params:
                    parameters.extend(more_params)
        
        return parameters

    def _extract_param_tail(self, node):
        """Extract parameters from <param_tail> node"""
        parameters = []
        
        data_type = None
        param_name = None
        
        for child in node.children:
            if child.value == "<data_type>":
                data_type = self._extract_data_type(child)
            elif child.value == "identifier":
                # Extract parameter name
                if hasattr(child, "lexeme"):
                    param_name = child.lexeme
                elif child.children and hasattr(child.children[0], "lexeme"):
                    param_name = child.children[0].lexeme
                
                if data_type and param_name:
                    parameters.append((data_type, param_name))
                    data_type = None
                    param_name = None
            
            elif child.value == "<param_tail>":
                # Recursive processing for nested tails
                more_params = self._extract_param_tail(child)
                if more_params:
                    parameters.extend(more_params)
        
        return parameters

    def _analyze_statements(self, node):
        """Analyze statements in a block"""
        for child in node.children:
            if child.value == "<statement>":
                self._analyze_statement(child)

    def _analyze_statement(self, node):
        """Analyze a single statement"""
        for child in node.children:
            if child.value == "identifier":
                # Variable usage or function call
                self._analyze_identifier_statement(node)
            elif child.value == "spit":
                # Return statement
                self._analyze_return_statement(node)
            elif child.value == "<conditional_statement>":
                # If/else statement
                self._analyze_conditional(child)
            elif child.value == "<looping_statement>":
                # Loop statement
                self._analyze_loop(child)
            elif child.value == "serve":
                # Print statement
                self._analyze_serve(child)
            elif child.value in ["++", "--"]:
                # Increment/decrement
                self._analyze_unary_operation(node)

    def _analyze_identifier_statement(self, node):
        """Analyze a statement starting with an identifier"""
        identifier = None
        line = -1
        
        # Extract the identifier
        identifier_node = self._find_child_by_value(node, "identifier")
        if identifier_node:
            if hasattr(identifier_node, "lexeme"):
                identifier = identifier_node.lexeme
                line = identifier_node.line
            elif identifier_node.children and hasattr(identifier_node.children[0], "lexeme"):
                identifier = identifier_node.children[0].lexeme
                line = identifier_node.children[0].line
        
        if identifier is None:
            return  # Can't process without an identifier
        
        # Check if it's a function call
        if self._find_child_by_value(node, "("):
            self._analyze_function_call(node, identifier, line)
        # Check if it's an array access
        elif self._find_child_by_value(node, "["):
            self._analyze_array_access(node, identifier, line)
        # Otherwise, it's a variable assignment
        else:
            self._analyze_assignment(node, identifier, line)

    def _analyze_function_call(self, node, function_name, line):
        """Analyze a function call"""
        # Check if function exists
        if function_name not in self.function_table:
            self.errors.append(f"Semantic Error at line {line}: Function '{function_name}' not declared")
            return
        
        # Extract arguments
        arguments = self._extract_arguments(node)
        
        # Check argument count
        expected_params = self.function_table[function_name]["params"]
        if len(arguments) != len(expected_params):
            self.errors.append(f"Semantic Error at line {line}: Function '{function_name}' expects {len(expected_params)} arguments, got {len(arguments)}")
            return
        
        # Check argument types
        for i, (arg_type, arg_value) in enumerate(arguments):
            expected_type = expected_params[i][0]
            if not self._is_compatible_type(arg_type, expected_type):
                self.errors.append(f"Semantic Error at line {line}: Type mismatch in argument {i+1} of function '{function_name}': expected {expected_type}, got {arg_type}")

    def _extract_arguments(self, node):
        """Extract arguments from a function call"""
        arguments = []
        
        # Find the argument list
        arg_list_node = self._find_child_by_value(node, "<argument_list>")
        if arg_list_node:
            # Process each argument
            for child in arg_list_node.children:
                if child.value == "<arithmetic_exp>":
                    arg_info = self._analyze_expression(child)
                    if arg_info:
                        arguments.append((arg_info["type"], arg_info["value"]))
                elif child.value == "<argument_tail>":
                    more_args = self._extract_argument_tail(child)
                    if more_args:
                        arguments.extend(more_args)
        
        return arguments

    def _extract_argument_tail(self, node):
        """Extract arguments from <argument_tail> node"""
        arguments = []
        
        for child in node.children:
            if child.value == "<arithmetic_exp>":
                arg_info = self._analyze_expression(child)
                if arg_info:
                    arguments.append((arg_info["type"], arg_info["value"]))
            elif child.value == "<argument_tail>":
                more_args = self._extract_argument_tail(child)
                if more_args:
                    arguments.extend(more_args)
        
        return arguments

    def _analyze_array_access(self, node, array_name, line):
        """Analyze array access"""
        # Check if the array exists
        array_found = False
        array_type = None
        array_size = None
        
        # Check in all scopes from current to global
        for scope in reversed(self.scopes):
            symbol_key = f"{scope}.{array_name}"
            if symbol_key in self.arrays:
                array_found = True
                array_type = self.arrays[symbol_key]["type"]
                array_size = self.arrays[symbol_key]["size"]
                break
        
        if not array_found:
            self.errors.append(f"Semantic Error at line {line}: Array '{array_name}' not declared")
            return None
        
        # Extract index
        index_node = self._find_child_by_value(node, "pinchliterals")
        index = None
        
        if index_node:
            if hasattr(index_node, "lexeme"):
                index = int(index_node.lexeme)
            elif index_node.children and hasattr(index_node.children[0], "lexeme"):
                index = int(index_node.children[0].lexeme)
        
        # Check if index is valid
        if index is not None and (index < 0 or index >= array_size):
            self.errors.append(f"Semantic Error at line {line}: Array index {index} out of bounds for array '{array_name}' with size {array_size}")
        
        # Check for assignment
        assignment_op_node = self._find_child_by_value(node, "<assignment_op>")
        if assignment_op_node:
            # This is an array assignment
            expression_node = self._find_child_by_value(node, "<arithmetic_exp>")
            if expression_node:
                expr_info = self._analyze_expression(expression_node)
                if expr_info and not self._is_compatible_type(expr_info["type"], array_type):
                    self.errors.append(f"Semantic Error at line {line}: Type mismatch in array assignment to '{array_name}[{index}]': expected {array_type}, got {expr_info['type']}")
        
        return {"type": array_type, "index": index}

    def _analyze_assignment(self, node, variable_name, line):
        """Analyze variable assignment"""
        # Check if the variable exists
        var_found = False
        var_type = None
        
        # Check in all scopes from current to global
        for scope in reversed(self.scopes):
            symbol_key = f"{scope}.{variable_name}"
            if symbol_key in self.symbol_table:
                var_found = True
                var_type = self.symbol_table[symbol_key]["type"]
                # Mark as initialized
                self.symbol_table[symbol_key]["initialized"] = True
                break
        
        if not var_found:
            self.errors.append(f"Semantic Error at line {line}: Variable '{variable_name}' not declared")
            return None
        
        # Extract assignment operator
        assignment_op_node = self._find_child_by_value(node, "<assignment_op>")
        if not assignment_op_node:
            return {"type": var_type, "name": variable_name}
        
        # Extract expression being assigned
        expression_node = self._find_child_by_value(node, "<expression>")
        if expression_node:
            expr_info = self._analyze_expression(expression_node)
            if expr_info and not self._is_compatible_type(expr_info["type"], var_type):
                self.errors.append(f"Semantic Error at line {line}: Type mismatch in assignment to '{variable_name}': expected {var_type}, got {expr_info['type']}")
        
        return {"type": var_type, "name": variable_name}

    def _analyze_expression(self, node):
        """Analyze an expression or arithmetic expression"""
        if node.value == "<expression>":
            # Complex expression with operators
            operand_node = self._find_child_by_value(node, "<expression_operand>")
            if operand_node:
                operand_info = self._analyze_expression_operand(operand_node)
                
                # Check for expression_tail with operators
                tail_node = self._find_child_by_value(node, "<expression_tail>")
                if tail_node and operand_info:
                    return self._analyze_expression_with_operators(operand_info, tail_node)
                
                return operand_info
        
        elif node.value == "<arithmetic_exp>":
            # Arithmetic expression
            operand_node = self._find_child_by_value(node, "<arithmetic_operand>")
            if operand_node:
                operand_info = self._analyze_arithmetic_operand(operand_node)
                
                # Check for arithmetic_tail with operators
                tail_node = self._find_child_by_value(node, "<arithmetic_tail>")
                if tail_node and operand_info:
                    return self._analyze_arithmetic_with_operators(operand_info, tail_node)
                
                return operand_info
        
        return None

    def _analyze_expression_operand(self, node):
        """Analyze an expression operand"""
        for child in node.children:
            if child.value == "<value>":
                return self._analyze_value(child)
            elif child.value == "(":
                # Nested expression
                expr_node = self._find_sibling_after(node.children, child, "<expression>")
                if expr_node:
                    return self._analyze_expression(expr_node)
            elif child.value in ["!", "!!"]:
                # Logical not
                expr_node = self._find_sibling_after(node.children, child, "<expression>")
                if expr_node:
                    expr_info = self._analyze_expression(expr_node)
                    if expr_info and expr_info["type"] != "bool":
                        line = -1
                        if hasattr(child, "line"):
                            line = child.line
                        self.errors.append(f"Semantic Error at line {line}: Logical not operator can only be applied to boolean expressions")
                    return {"type": "bool", "value": None}
        
        return None

    def _analyze_arithmetic_operand(self, node):
        """Analyze an arithmetic operand"""
        for child in node.children:
            if child.value == "<value2>":
                return self._analyze_value2(child)
            elif child.value == "(":
                # Nested expression
                expr_node = self._find_sibling_after(node.children, child, "<arithmetic_exp>")
                if expr_node:
                    return self._analyze_expression(expr_node)
        
        return None

    def _analyze_value(self, node):
        """Analyze a value (can be literal, variable, or function call)"""
        for child in node.children:
            if child.value == "<literals>":
                return self._extract_literal_value(child)
            elif child.value == "identifier":
                # Get identifier name
                identifier = None
                line = -1
                
                if hasattr(child, "lexeme"):
                    identifier = child.lexeme
                    line = child.line
                elif child.children and hasattr(child.children[0], "lexeme"):
                    identifier = child.children[0].lexeme
                    line = child.children[0].line
                
                if identifier is None:
                    continue
                
                # Check if it's followed by ( for function call
                tail_node = self._find_child_by_value(node, "<value_identifier_tail>")
                if tail_node:
                    if self._find_child_by_value(tail_node, "("):
                        # Function call
                        if identifier not in self.function_table:
                            self.errors.append(f"Semantic Error at line {line}: Function '{identifier}' not declared")
                            return None
                        
                        # Check arguments
                        self._analyze_function_call_args(tail_node, identifier, line)
                        
                        return {"type": self.function_table[identifier]["return_type"], "value": None}
                    
                    elif self._find_child_by_value(tail_node, "["):
                        # Array access
                        return self._analyze_array_value(identifier, tail_node, line)
                
                # Variable reference
                var_found = False
                var_type = None
                
                # Check in all scopes from current to global
                for scope in reversed(self.scopes):
                    symbol_key = f"{scope}.{identifier}"
                    if symbol_key in self.symbol_table:
                        var_found = True
                        var_type = self.symbol_table[symbol_key]["type"]
                        
                        # Check if variable is initialized
                        if not self.symbol_table[symbol_key]["initialized"]:
                            self.errors.append(f"Semantic Error at line {line}: Variable '{identifier}' used before initialization")
                        
                        break
                
                if not var_found:
                    self.errors.append(f"Semantic Error at line {line}: Variable '{identifier}' not declared")
                    return None
                
                return {"type": var_type, "value": None}
        
        return None

    def _analyze_value2(self, node):
        """Analyze a value2 (similar to value but without boolean literals)"""
        for child in node.children:
            if child.value == "<literals2>":
                # Extract non-boolean literal
                for lit_child in child.children:
                    if lit_child.value in ["pinchliterals", "skimliterals", "pastaliterals"]:
                        value = None
                        if hasattr(lit_child, "lexeme"):
                            value = lit_child.lexeme
                        elif lit_child.children and hasattr(lit_child.children[0], "lexeme"):
                            value = lit_child.children[0].lexeme
                        
                        # Map literal type to variable type
                        type_map = {
                            "pinchliterals": "pinch",
                            "skimliterals": "skim",
                            "pastaliterals": "pasta"
                        }
                        return {"type": type_map[lit_child.value], "value": value}
            
            elif child.value == "identifier":
                # Similar to _analyze_value but without boolean processing
                return self._analyze_value(node)
        
        return None

    def _analyze_array_value(self, array_name, tail_node, line):
        """Analyze array access as a value"""
        # Check if the array exists
        array_found = False
        array_type = None
        array_size = None
        
        # Check in all scopes from current to global
        for scope in reversed(self.scopes):
            symbol_key = f"{scope}.{array_name}"
            if symbol_key in self.arrays:
                array_found = True
                array_type = self.arrays[symbol_key]["type"]
                array_size = self.arrays[symbol_key]["size"]
                break
        
        if not array_found:
            self.errors.append(f"Semantic Error at line {line}: Array '{array_name}' not declared")
            return None
        
        # Extract index
        index_node = self._find_child_by_value(tail_node, "pinchliterals")
        index = None
        
        if index_node:
            if hasattr(index_node, "lexeme"):
                index = int(index_node.lexeme)
            elif index_node.children and hasattr(index_node.children[0], "lexeme"):
                index = int(index_node.children[0].lexeme)
        
        # Check if index is valid
        if index is not None and (index < 0 or index >= array_size):
            self.errors.append(f"Semantic Error at line {line}: Array index {index} out of bounds for array '{array_name}' with size {array_size}")
        
        return {"type": array_type, "value": None}

    def _analyze_function_call_args(self, tail_node, function_name, line):
        """Analyze arguments in a function call"""
        # Extract arguments
        arg_list_node = self._find_child_by_value(tail_node, "<argument_list>")
        if not arg_list_node:
            # No arguments
            if self.function_table[function_name]["params"]:
                self.errors.append(f"Semantic Error at line {line}: Function '{function_name}' expects {len(self.function_table[function_name]['params'])} arguments, got 0")
            return
        
        arguments = self._extract_arguments_from_list(arg_list_node)
        
        # Check argument count
        expected_params = self.function_table[function_name]["params"]
        if len(arguments) != len(expected_params):
            self.errors.append(f"Semantic Error at line {line}: Function '{function_name}' expects {len(expected_params)} arguments, got {len(arguments)}")
            return
        
        # Check argument types
        for i, (arg_type, arg_value) in enumerate(arguments):
            expected_type = expected_params[i][0]
            if not self._is_compatible_type(arg_type, expected_type):
                self.errors.append(f"Semantic Error at line {line}: Type mismatch in argument {i+1} of function '{function_name}': expected {expected_type}, got {arg_type}")

    def _extract_arguments_from_list(self, node):
        """Extract arguments from an argument list node"""
        arguments = []
        
        for child in node.children:
            if child.value == "<expression>":
                expr_info = self._analyze_expression(child)
                if expr_info:
                    arguments.append((expr_info["type"], expr_info["value"]))
            elif child.value == "<argument_tail>":
                more_args = self._extract_argument_tail(child)
                if more_args:
                    arguments.extend(more_args)
        
        return arguments

    def _analyze_expression_with_operators(self, left_operand, tail_node):
        """Analyze expression with operators in the tail"""
        result_type = left_operand["type"]
        
        # Process operators
        for child in tail_node.children:
            if child.value in ["&&", "||"]:
                # Logical operators require boolean operands
                if result_type != "bool":
                    line = -1
                    if hasattr(child, "line"):
                        line = child.line
                    self.errors.append(f"Semantic Error at line {line}: Logical operator requires boolean operands, got {result_type}")
                
                # Right operand must be boolean
                right_operand_node = self._find_sibling_after(tail_node.children, child, "<expression_operand>")
                if right_operand_node:
                    right_info = self._analyze_expression_operand(right_operand_node)
                    if right_info and right_info["type"] != "bool":
                        line = -1
                        if hasattr(child, "line"):
                            line = child.line
                        self.errors.append(f"Semantic Error at line {line}: Logical operator requires boolean operands, got {right_info['type']}")
                
                # Result of logical operation is boolean
                result_type = "bool"
            
            elif child.value in ["==", "!=", "<", ">", "<=", ">="]:
                # Comparison operators
                right_operand_node = self._find_sibling_after(tail_node.children, child, "<expression_operand>")
                if right_operand_node:
                    right_info = self._analyze_expression_operand(right_operand_node)
                    if right_info and not self._is_comparable_type(left_operand["type"], right_info["type"]):
                        line = -1
                        if hasattr(child, "line"):
                            line = child.line
                        self.errors.append(f"Semantic Error at line {line}: Cannot compare values of types {left_operand['type']} and {right_info['type']}")
                
                # Result of comparison is boolean
                result_type = "bool"
        
        return {"type": result_type, "value": None}

    def _analyze_arithmetic_with_operators(self, left_operand, tail_node):
        """Analyze arithmetic expression with operators in the tail"""
        result_type = left_operand["type"]
        
        # Process operators
        for child in tail_node.children:
            if child.value in ["+", "-", "*", "/", "%"]:
                # Arithmetic operators
                right_operand_node = self._find_sibling_after(tail_node.children, child, "<arithmetic_operand>")
                if right_operand_node:
                    right_info = self._analyze_arithmetic_operand(right_operand_node)
                    if right_info:
                        # Check if the operation is valid for these types
                        if not self._is_arithmetic_compatible(left_operand["type"], right_info["type"], child.value):
                            line = -1
                            if hasattr(child, "line"):
                                line = child.line
                            self.errors.append(f"Semantic Error at line {line}: Cannot perform arithmetic operation '{child.value}' on types {left_operand['type']} and {right_info['type']}")
                        
                        # Determine result type (promotion rules)
                        result_type = self._get_arithmetic_result_type(left_operand["type"], right_info["type"])
        
        return {"type": result_type, "value": None}

    def _is_arithmetic_compatible(self, type1, type2, operator):
        """Check if arithmetic operation is valid for the given types"""
        numeric_types = ["pinch", "skim"]
        
        if operator == "+":
            # Special case for + with pasta (string concatenation)
            if type1 == "pasta" and type2 == "pasta":
                return True
            return type1 in numeric_types and type2 in numeric_types
        
        # Other arithmetic operators only work with numeric types
        return type1 in numeric_types and type2 in numeric_types

    def _get_arithmetic_result_type(self, type1, type2):
        """Determine result type of arithmetic operation based on type promotion rules"""
        if type1 == "pasta" and type2 == "pasta":
            return "pasta"
        
        # Type promotion: skim takes precedence over pinch
        if "skim" in [type1, type2]:
            return "skim"
        
        return "pinch"

    def _is_compatible_type(self, source_type, target_type):
        """Check if source_type is compatible with target_type"""
        print(f"DEBUG: Checking type compatibility: {source_type} vs {target_type}")
        # Same types are always compatible
        if source_type == target_type:
            print("DEBUG: Types are identical, compatible")
            return True
            
        # Different types are not compatible
        print("DEBUG: Types are different, incompatible")
        return False

    def _analyze_return_statement(self, node):
        """Analyze a return statement"""
        if self.current_function is None:
            # Return statement outside of function
            line = -1
            for child in node.children:
                if hasattr(child, "line"):
                    line = child.line
                    break
            self.errors.append(f"Semantic Error at line {line}: Return statement outside of function")
            return
        
        # Mark the function as having a return statement
        self.function_table[self.current_function]["has_return"] = True
        
        # Get the return type of the current function
        expected_type = self.function_table[self.current_function]["return_type"]
        
        # Check if it's a void function
        if expected_type == "hungry":
            # Void functions shouldn't return a value
            expr_node = self._find_child_by_value(node, "<expression>")
            if expr_node:
                line = -1
                for child in node.children:
                    if hasattr(child, "line"):
                        line = child.line
                        break
                self.errors.append(f"Semantic Error at line {line}: Void function '{self.current_function}' cannot return a value")
            return
        
        # Non-void functions must return a value of the correct type
        expr_node = self._find_child_by_value(node, "<expression>")
        if not expr_node:
            line = -1
            for child in node.children:
                if hasattr(child, "line"):
                    line = child.line
                    break
            self.errors.append(f"Semantic Error at line {line}: Function '{self.current_function}' must return a value of type {expected_type}")
            return
        
        # Analyze the return expression
        expr_info = self._analyze_expression(expr_node)
        if expr_info and not self._is_compatible_type(expr_info["type"], expected_type):
            line = -1
            for child in node.children:
                if hasattr(child, "line"):
                    line = child.line
                    break
            self.errors.append(f"Semantic Error at line {line}: Type mismatch in return statement: expected {expected_type}, got {expr_info['type']}")

    def _analyze_conditional(self, node):
        """Analyze a conditional statement (if/else)"""
        # Find the condition
        condition_node = self._find_child_by_value(node, "<expression>")
        if condition_node:
            condition_info = self._analyze_expression(condition_node)
            if condition_info and condition_info["type"] != "bool":
                line = -1
                if_node = self._find_child_by_value(node, "if")
                if if_node and hasattr(if_node, "line"):
                    line = if_node.line
                self.errors.append(f"Semantic Error at line {line}: Condition must be a boolean expression, got {condition_info['type']}")
        
        # Analyze the statement blocks
        for child in node.children:
            if child.value == "<statement_block>":
                self._analyze_statements(child)

    def _analyze_loop(self, node):
        """Analyze a looping statement"""
        # Find loop type
        while_node = self._find_child_by_value(node, "while")
        for_node = self._find_child_by_value(node, "for")
        
        if while_node:
            # While loop
            condition_node = self._find_child_by_value(node, "<expression>")
            if condition_node:
                condition_info = self._analyze_expression(condition_node)
                if condition_info and condition_info["type"] != "bool":
                    line = -1
                    if hasattr(while_node, "line"):
                        line = while_node.line
                    self.errors.append(f"Semantic Error at line {line}: While loop condition must be a boolean expression, got {condition_info['type']}")
        
        elif for_node:
            # For loop
            # Initialize new scope for for-loop variables
            for_scope = f"{self.current_scope}_for_{len(self.scopes)}"
            self.scopes.append(for_scope)
            self.current_scope = for_scope
            
            # Analyze initialization
            init_node = self._find_child_by_value(node, "<for_init>")
            if init_node:
                self._analyze_for_init(init_node)
            
            # Analyze condition
            condition_node = self._find_child_by_value(node, "<expression>")
            if condition_node:
                condition_info = self._analyze_expression(condition_node)
                if condition_info and condition_info["type"] != "bool":
                    line = -1
                    if hasattr(for_node, "line"):
                        line = for_node.line
                    self.errors.append(f"Semantic Error at line {line}: For loop condition must be a boolean expression, got {condition_info['type']}")
            
            # Analyze iteration
            iter_node = self._find_child_by_value(node, "<for_iter>")
            if iter_node:
                self._analyze_for_iter(iter_node)
            
            # Restore previous scope after analyzing the body
            statement_block = self._find_child_by_value(node, "<statement_block>")
            if statement_block:
                self._analyze_statements(statement_block)
            
            # Pop the for-loop scope
            self.scopes.pop()
            self.current_scope = self.scopes[-1]
            
        # Analyze the statement block
        statement_block = self._find_child_by_value(node, "<statement_block>")
        if statement_block:
            self._analyze_statements(statement_block)

    def _analyze_for_init(self, node):
        """Analyze for loop initialization"""
        # Can be a declaration or an assignment
        for child in node.children:
            if child.value == "<declarations>":
                self._analyze_declaration(child, self.current_scope)
            elif child.value == "identifier":
                # Assignment to existing variable
                identifier = None
                line = -1
                
                if hasattr(child, "lexeme"):
                    identifier = child.lexeme
                    line = child.line
                elif child.children and hasattr(child.children[0], "lexeme"):
                    identifier = child.children[0].lexeme
                    line = child.children[0].line
                
                if identifier:
                    self._analyze_assignment(node, identifier, line)

    def _analyze_for_iter(self, node):
        """Analyze for loop iteration expression"""
        # Can be an assignment or increment/decrement
        for child in node.children:
            if child.value == "identifier":
                # Assignment or increment/decrement
                identifier = None
                line = -1
                
                if hasattr(child, "lexeme"):
                    identifier = child.lexeme
                    line = child.line
                elif child.children and hasattr(child.children[0], "lexeme"):
                    identifier = child.children[0].lexeme
                    line = child.children[0].line
                
                if identifier:
                    if self._find_child_by_value(node, "++") or self._find_child_by_value(node, "--"):
                        self._analyze_unary_operation(node)
                    else:
                        self._analyze_assignment(node, identifier, line)

    def _analyze_serve(self, node):
        """Analyze a serve (print) statement"""
        # Extract the expression to be printed
        expr_node = self._find_child_by_value(node, "<expression>")
        if expr_node:
            self._analyze_expression(expr_node)

    def _analyze_unary_operation(self, node):
        """Analyze unary operations (++, --)"""
        # Find identifier
        identifier_node = self._find_child_by_value(node, "identifier")
        if not identifier_node:
            return
        
        identifier = None
        line = -1
        
        if hasattr(identifier_node, "lexeme"):
            identifier = identifier_node.lexeme
            line = identifier_node.line
        elif identifier_node.children and hasattr(identifier_node.children[0], "lexeme"):
            identifier = identifier_node.children[0].lexeme
            line = identifier_node.children[0].line
        
        if identifier is None:
            return
        
        # Check if variable exists
        var_found = False
        var_type = None
        
        # Check in all scopes from current to global
        for scope in reversed(self.scopes):
            symbol_key = f"{scope}.{identifier}"
            if symbol_key in self.symbol_table:
                var_found = True
                var_type = self.symbol_table[symbol_key]["type"]
                break
        
        if not var_found:
            self.errors.append(f"Semantic Error at line {line}: Variable '{identifier}' not declared")
            return
        
        # Check if variable type is numeric
        if var_type not in ["pinch", "skim"]:
            self.errors.append(f"Semantic Error at line {line}: Increment/decrement operations can only be applied to numeric types, got {var_type}")

    def _is_compatible_type(self, source_type, target_type):
        """Check if source_type is compatible with target_type"""
        if source_type == target_type:
            return True
        
        # Numeric type conversion rules
        if source_type == "pinch" and target_type == "skim":
            return True  # pinch can be implicitly converted to skim
        
        return False

    def _find_child_by_value(self, node, value):
        """Find a child node with the specified value"""
        print(f"DEBUG: Finding child with value: {value} in {node.value}")
        for child in node.children:
            if child.value == value:
                print(f"DEBUG: Found child with value: {value}")
                return child
        print(f"DEBUG: Child with value {value} not found")
        return None

    def _find_sibling_after(self, siblings, current, value):
        """Find the first sibling after current with the given value"""
        found_current = False
        for sibling in siblings:
            if sibling == current:
                found_current = True
                continue
            
            if found_current and hasattr(sibling, "value") and sibling.value == value:
                return sibling
        
        return None
    
    def _check_type_compatibility(self, expected_type, actual_type, variable_name, line_number):
        if expected_type != actual_type:
            error_msg = f"Semantic Error at line {line_number}: Type mismatch in initialization of '{variable_name}': expected {expected_type}, got {actual_type}"
            self.errors.append(error_msg)
            return False
        return True
    
class SimpleNode:
    def __init__(self, children):
        self.value = "declaration"
        self.children = children
