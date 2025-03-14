class SyntaxErrorHandler:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.semantic_errors = []
        
        # Keep track of current context for better error messages
        self.current_context = None
        self.current_function = None
        
        # Rules specific to the language
        self.reserved_words = {
            "full": "used only with non-void functions that return a value",
            "hungry": "used for void functions that don't return a value",
            "chef": "required for the main function declaration",
            "dinein": "required at the beginning of the program",
            "takeout": "required at the end of the program",
            "spit": "required for returning values from functions"
        }
        
        # Keep track of valid data types for type checking
        self.valid_data_types = ["pinch", "skim", "pasta", "bool"]
    
    def syntax_error(self, line_number, found, expected, stack=None):
        """Record a syntax error with detailed information about the error location and expected tokens."""
        # Get the actual lexeme for better error messages
        token_lexeme = found
        
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
        if not stack:
            # Stack is empty, but we still have tokens → unexpected extra tokens
            error_message = f"Syntax Error at line {line_number}: Unexpected token '{token_lexeme}' after parsing completed"
        elif found == '$' and stack and stack[-1] != '$':
            # Unexpected end of input - something is missing
            top_symbol = stack[-1]
            missing_desc = f"'{top_symbol}'" if not (isinstance(top_symbol, str) and top_symbol.startswith("<")) else "required tokens"
            error_message = f"Syntax Error at line {line_number}: Unexpected end of input, missing {missing_desc}"
        elif filtered_expected:
            # We have expected tokens to report
            expected_str = ", ".join(f"'{e}'" for e in filtered_expected)
            error_message = f"Syntax Error at line {line_number}: Unexpected '{token_lexeme}', expected {expected_str}"
        else:
            # No specific expected tokens to report
            error_message = f"Syntax Error at line {line_number}: Unexpected '{token_lexeme}'"
        
        # Add context about current parsing state
        if self.current_context:
            error_message += f" while parsing <{self.current_context}>"
        
        # Add a recovery hint if possible
        if filtered_expected and len(filtered_expected) <= 3:
            error_message += f" - consider adding {' or '.join(f"'{e}'" for e in filtered_expected)}"
        
        # Check for special cases related to the language
        if token_lexeme in self.reserved_words and self.current_context:
            error_message += f". Note: '{token_lexeme}' is {self.reserved_words[token_lexeme]}"
        
        self.errors.append(error_message)
        return error_message
    
    def semantic_error(self, line_number, message, context=None):
        """Record semantic errors that relate to language rules rather than syntax."""
        context_info = f" in {context}" if context else ""
        error_message = f"Semantic Error at line {line_number}: {message}{context_info}"
        self.semantic_errors.append(error_message)
        return error_message
    
    def warning(self, line_number, message):
        """Record non-critical issues that might cause problems."""
        warning_message = f"Warning at line {line_number}: {message}"
        self.warnings.append(warning_message)
        return warning_message
    
    def function_declaration_error(self, line_number, function_name, function_type, declaration_keyword):
        """Specific error for function declaration issues."""
        if declaration_keyword == "full" and function_type == "hungry":
            return self.semantic_error(line_number, 
                f"Function '{function_name}' is declared with 'full' but doesn't return a value", 
                "function declaration")
        elif declaration_keyword == "hungry" and function_type != "hungry":
            return self.semantic_error(line_number, 
                f"Function '{function_name}' is declared with 'hungry' but should return a value", 
                "function declaration")
        elif declaration_keyword not in ["full", "hungry"]:
            return self.syntax_error(line_number, declaration_keyword, ["full", "hungry"])
    
    def check_return_statement(self, line_number, function_name, function_type, has_return):
        """Check if return statements match function type."""
        if function_type != "hungry" and not has_return:
            return self.semantic_error(line_number, 
                f"Non-void function '{function_name}' must have a 'spit' statement", 
                "function body")
        elif function_type == "hungry" and has_return:
            return self.warning(line_number, 
                f"Void function '{function_name}' should not have a 'spit' statement")
    
    def update_context(self, context, function_name=None):
        """Update the current parsing context for better error messages."""
        self.current_context = context
        if function_name:
            self.current_function = function_name
    
    def get_all_errors(self):
        """Return all errors and warnings in a structured format."""
        return {
            "syntax_errors": self.errors,
            "semantic_errors": self.semantic_errors,
            "warnings": self.warnings,
            "total_errors": len(self.errors) + len(self.semantic_errors),
            "total_warnings": len(self.warnings)
        }
    
    def get_error_summary(self):
        """Return a summary of all errors and warnings."""
        if not self.errors and not self.semantic_errors and not self.warnings:
            return "No errors or warnings detected."
        
        summary = []
        if self.errors:
            summary.append(f"Found {len(self.errors)} syntax errors:")
            for i, error in enumerate(self.errors, 1):
                summary.append(f"  {i}. {error}")
        
        if self.semantic_errors:
            summary.append(f"Found {len(self.semantic_errors)} semantic errors:")
            for i, error in enumerate(self.semantic_errors, 1):
                summary.append(f"  {i}. {error}")
        
        if self.warnings:
            summary.append(f"Found {len(self.warnings)} warnings:")
            for i, warning in enumerate(self.warnings, 1):
                summary.append(f"  {i}. {warning}")
        
        return "\n".join(summary)
    
    def clear(self):
        """Clear all errors and warnings."""
        self.errors = []
        self.semantic_errors = []
        self.warnings = []
        self.current_context = None
        self.current_function = None