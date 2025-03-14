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
            return False, self.errors

        print("Starting semantic analysis...")
        print(f"Parse Tree Root: {parse_tree.value}")
        self.output_messages.append("Starting semantic analysis...")

        # Start the analysis with the root node
        self._analyze_node(parse_tree, is_root=True)

        # Check for function return statements
        for func_name, func_info in self.function_table.items():
            if func_info["return_type"] != "hungry" and not func_info.get("has_return", False):
                error_msg = f"Semantic Error: Function '{func_name}' must return a value of type {func_info['return_type']}"
                self.errors.append(error_msg)
                self.output_messages.append(error_msg)

        if self.errors:
            return False, self.errors

        self.output_messages.append("Semantic analysis completed successfully!")
        return True, self.output_messages

    def _analyze_node(self, node, is_root=False):
        if not node:
            return
            
        # Add debugging to help track the node traversal
        print(f"Analyzing node: {node.value if hasattr(node, 'value') else 'None'}")
        
        if not hasattr(node, "value"):
            print(f"Node has no value attribute: {node}")
            return

        # Process the current node based on its type
        if node.value == "<program>":
            if is_root:
                self._analyze_program(node)
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
        elif node.value == "<statement>":
            self._analyze_statement(node)
            self.output_messages.append("Processed statement")
        
        # Check if node has children before traversing
        if hasattr(node, "children"):
            if node.children:
                self.output_messages.append(f"Traversing {len(node.children)} children of {node.value}")
                for child in node.children:
                    self._analyze_node(child)
        else:
            print(f"Node has no children attribute: {node.value}")

    def _analyze_program(self, node):
        # First, ensure we have children to process
        if not hasattr(node, "children") or not node.children:
            self.errors.append("Semantic Error: Empty program")
            return
            
        # Check for dinein and takeout keywords
        tokens = self._extract_all_tokens(node)
        
        if not tokens or "dinein" not in tokens:
            self.errors.append("Semantic Error: Missing 'dinein' at the beginning of the program")
        if not tokens or "takeout" not in tokens:
            self.errors.append("Semantic Error: Missing 'takeout' at the end of the program")
    
    def _extract_all_tokens(self, node):
        """Extract all token values from a node and its children"""
        tokens = []
        if not hasattr(node, "value"):
            return tokens
            
        # Add this node's value if it's a token (not a non-terminal)
        if not node.value.startswith("<") and not node.value.startswith("'<"):
            tokens.append(node.value)
            
        # Recursively add children's tokens
        if hasattr(node, "children"):
            for child in node.children:
                tokens.extend(self._extract_all_tokens(child))
                
        return tokens

    def _analyze_functions(self, node):
        """Analyze function declarations and definitions"""
        # Reset current scope for a new function
        function_name = None
        return_type = None
        
        # Extract function information from children
        for i, child in enumerate(node.children):
            if hasattr(child, "value"):
                if child.value == "hungry" or child.value == "pinch" or child.value == "platter":
                    return_type = child.value
                elif return_type and function_name is None and not child.value.startswith("<"):
                    function_name = child.value
                    self.current_function = function_name
                    self.current_scope = function_name
                    self.scopes.append(function_name)
                    
                    # Register function in function table
                    self.function_table[function_name] = {
                        "return_type": return_type,
                        "parameters": [],
                        "has_return": False
                    }
                    
                    self.output_messages.append(f"Registered function: {function_name} with return type: {return_type}")
                    
                    break
                    
        # Process parameters if we found a function
        if function_name:
            param_node = self._find_node(node, "<parameters>")
            if param_node:
                self._analyze_parameters(param_node, function_name)

    def _find_node(self, parent, node_value):
        """Find a child node with the specified value"""
        if not hasattr(parent, "children"):
            return None
            
        for child in parent.children:
            if hasattr(child, "value") and child.value == node_value:
                return child
        return None

    def _analyze_parameters(self, node, function_name):
        """Analyze function parameters"""
        current_type = None
        
        for i, child in enumerate(node.children):
            if not hasattr(child, "value"):
                continue
                
            if child.value == "pinch" or child.value == "platter":
                current_type = child.value
            elif current_type and not child.value.startswith("<") and child.value != "," and child.value != ")":
                # This is a parameter name
                param_name = child.value
                
                # Add to function table
                self.function_table[function_name]["parameters"].append({
                    "name": param_name,
                    "type": current_type
                })
                
                # Add to symbol table
                self.symbol_table[param_name] = {
                    "type": current_type,
                    "scope": function_name
                }
                
                self.output_messages.append(f"Added parameter: {param_name} of type {current_type} to function {function_name}")

    def _analyze_function_definition(self, node):
        """Analyze function definition (body)"""
        # The implementation depends on your language's specific structure
        pass

    def _analyze_global_declarations(self, node):
        """Analyze global variable declarations"""
        self._analyze_declarations(node, "global")

    def _analyze_local_declarations(self, node):
        """Analyze local variable declarations"""
        self._analyze_declarations(node, self.current_scope)

    def _analyze_declarations(self, node, scope):
        """Generic method to analyze variable declarations"""
        current_type = None
        
        for child in node.children:
            if not hasattr(child, "value"):
                continue
                
            if child.value == "pinch" or child.value == "platter":
                current_type = child.value
            elif current_type and not child.value.startswith("<") and child.value != ";" and child.value != ",":
                # This is a variable name
                var_name = child.value
                
                # Check for redeclaration
                if var_name in self.symbol_table and self.symbol_table[var_name]["scope"] == scope:
                    self.errors.append(f"Semantic Error: Variable '{var_name}' already declared in scope '{scope}'")
                else:
                    # Add to symbol table
                    self.symbol_table[var_name] = {
                        "type": current_type,
                        "scope": scope
                    }
                    
                    self.output_messages.append(f"Added variable: {var_name} of type {current_type} to scope {scope}")

    def _analyze_statements(self, node):
        """Analyze statements in a block"""
        for child in node.children:
            if hasattr(child, "value") and child.value == "<statement>":
                self._analyze_statement(child)
            
    def _analyze_statement(self, node):
        """Analyze a single statement"""
        # Extract the first token to determine statement type
        if not hasattr(node, "children") or not node.children:
            return
            
        statement_type = None
        for child in node.children:
            if hasattr(child, "value") and not child.value.startswith("<"):
                statement_type = child.value
                break
                
        if statement_type == "serve":
            self._analyze_serve_statement(node)
        elif statement_type == "spit":
            # Mark function as having a return statement
            if self.current_function:
                self.function_table[self.current_function]["has_return"] = True
            self._analyze_return_statement(node)
        elif statement_type:
            # This could be an assignment or function call
            self._analyze_assignment_or_call(node, statement_type)
            
    def _analyze_serve_statement(self, node):
        """Analyze a serve (print) statement"""
        # Implementation depends on your language
        pass
        
    def _analyze_return_statement(self, node):
        """Analyze a return statement"""
        # Implementation depends on your language
        pass
        
    def _analyze_assignment_or_call(self, node, identifier):
        """Analyze an assignment or function call"""
        # Check if the identifier exists in the symbol table
        if identifier not in self.symbol_table:
            # Check if it's a function call
            if identifier in self.function_table:
                self._analyze_function_call(node, identifier)
            else:
                self.errors.append(f"Semantic Error: Undeclared identifier '{identifier}'")
        else:
            # It's an assignment
            self._analyze_assignment(node, identifier)
            
    def _analyze_function_call(self, node, function_name):
        """Analyze a function call"""
        # Implementation depends on your language
        pass
        
    def _analyze_assignment(self, node, variable_name):
        """Analyze an assignment statement"""
        # Implementation depends on your language
        pass