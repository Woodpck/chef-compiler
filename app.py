from flask import Flask, render_template, request
from src.lexical.lexical import LexicalAnalyzer
from src.syntax.syntax import LL1Parser, cfg, parse_table, follow_set
# Import the semantic analyzer
from src.semantic.semantic import SemanticAnalyzer  # Adjust import path as needed

app = Flask(__name__)

def normalize_newlines(text):
    """Normalize newline characters for cross-platform compatibility."""
    return text.replace("\r\n", "\n").replace("\r", "\n")

@app.route("/", methods=["GET", "POST"])
def index():
    result = []  # Lexical tokens
    syntax_tokens = []  # Tokens for Syntax Analyzer
    error_tokens_text = ""
    error_syntax_text = ""
    error_semantic_text = ""  # New variable for semantic errors
    output = []  # Stores semantic analysis output
    identifier_count = 0  # Initialize identifier count
    code = ""  # Initialize code for all request types
    
    if request.method == "POST":
        code = normalize_newlines(request.form.get("code", ""))
        action = request.form.get("action")
        if action == "lexical" and code.strip():
            analyzer = LexicalAnalyzer()
            try:
                result = analyzer.tokenize(code)
                identifier_count = analyzer.identifier_count  # Get the count
                error_tokens_text = "\n".join(analyzer.errors) if hasattr(analyzer, 'errors') else ""
            except Exception as e:
                error_tokens_text = f"An error occurred: {e}"
                
        if action == "syntax" and code.strip():
            analyzer = LexicalAnalyzer()
            try:
                lexical_tokens = analyzer.tokenize(code)
                identifier_count = analyzer.identifier_count  # Get the count
                error_tokens_text = "\n".join(analyzer.errors) if hasattr(analyzer, 'errors') else ""
                
                if error_tokens_text:
                    result = lexical_tokens
                    error_syntax_text = "Cannot proceed with Syntax Analysis due to Lexical Errors"
                else:
                    # Track line numbers based on the original code
                    code_lines = code.splitlines()
                    line_positions = []
                    pos = 0
                    
                    # Build a map of character positions to line numbers
                    for i, line in enumerate(code_lines, 1):
                        line_len = len(line)
                        # Map each position in this line to its line number
                        for j in range(line_len + 1):  # +1 for the newline
                            line_positions.append(i)
                        pos += line_len + 1
                    
                    # Create syntax tokens with line numbers
                    syntax_tokens = []
                    pos = 0
                    
                    for lexeme, token in lexical_tokens:
                        # Search for the lexeme starting from current position
                        lexeme_pos = code.find(lexeme, pos)
                        
                        if lexeme_pos >= 0 and lexeme_pos < len(line_positions):
                            # Get the line number for this position
                            line_num = line_positions[lexeme_pos]
                            pos = lexeme_pos + len(lexeme)  # Move position past this token
                        else:
                            # Default to line 1 if we can't determine position
                            line_num = 1
                        
                        # Add token with line number
                        syntax_tokens.append((lexeme, token, line_num))
                    
                    # Store the original tokens for display
                    result = lexical_tokens
                    
                    # Debug: print tokens with line numbers
                    print("DEBUG: Tokens with line numbers:")
                    for i, t in enumerate(syntax_tokens):
                        print(f"  Token {i}: {t}")
                    
                    # Create the Parser instance with required parameters
                    parser = LL1Parser(cfg, parse_table, follow_set)
                    
                    # Parse using the tokens from lexical analysis
                    success, errors = parser.parse(syntax_tokens)
                    
                    # Check for syntax errors
                    if errors:
    # Format the error information better
                        if isinstance(errors, list) and errors:
                            error_syntax_text = "\n".join([str(error) for error in errors])
                        else:
                            error_syntax_text = "Syntax analysis failed with empty error list."
                    elif not success:
                        error_syntax_text = "Syntax analysis failed with no specific errors."
                    
            except Exception as e:
                import traceback
                error_tokens_text = f"Lexical Analysis Error: {e}"
                error_trace = traceback.format_exc()
                error_tokens_text += "\n" + error_trace
                
        elif action == "semantic" and code.strip():
            # First run lexical analysis
            analyzer = LexicalAnalyzer()
            try:
                lexical_tokens = analyzer.tokenize(code)
                identifier_count = analyzer.identifier_count
                error_tokens_text = "\n".join(analyzer.errors) if hasattr(analyzer, 'errors') and analyzer.errors else ""
                
                # Store the original tokens for display
                result = lexical_tokens
                
                if error_tokens_text:
                    error_semantic_text = "Cannot proceed with Semantic Analysis due to Lexical Errors"
                else:
                    # Run syntax analysis
                    syntax_tokens = []
                    for i, (lexeme, token) in enumerate(lexical_tokens, 1):
                        syntax_tokens.append((lexeme, token, i))
                    
                    # Create the Parser instance with required parameters
                    parser = LL1Parser(cfg, parse_table, follow_set)
                    
                    # Parse using the tokens from lexical analysis
                    syntax_success, syntax_errors = parser.parse(syntax_tokens)
                    
                    if not syntax_success:
                        error_syntax_text = "\n".join(syntax_errors) if syntax_errors else "Syntax analysis failed with no specific errors."
                        error_semantic_text = "Cannot proceed with Semantic Analysis due to Syntax Errors"
                    else:
                        # Now proceed with semantic analysis
                        try:
                            # Create semantic analyzer instance
                            semantic_analyzer = SemanticAnalyzer()
                            
                            # Check if parse tree exists and run analysis
                            if not parser.parse_tree:
                                error_semantic_text = "Parse tree not available for semantic analysis"
                                output = ["Semantic analysis failed: No parse tree available"]
                            else:
                                print("Running semantic analysis...")
                                # Run semantic analysis with parse tree
                                semantic_success, semantic_result = semantic_analyzer.analyze(parser.parse_tree)
                                
                                # IMPORTANT: Always get the output messages
                                output = semantic_analyzer.output_messages
                                
                                # Check for success and set error message if necessary
                                if not semantic_success:
                                    # This is a critical line - make sure the errors are joined correctly
                                    error_semantic_text = "\n".join(semantic_analyzer.errors)
                                    print(f"Semantic errors: {error_semantic_text}")  # Debug log
                                else:
                                    # Clear any previous semantic errors
                                    error_semantic_text = ""
                                
                        except Exception as e:
                            import traceback
                            error_semantic_text = f"Semantic Analysis Error: {e}"
                            error_trace = traceback.format_exc()
                            error_semantic_text += "\n" + error_trace
                            print(f"Semantic Analysis Exception: {e}")
                            print(error_trace)
            
            except Exception as e:
                import traceback
                error_tokens_text = f"Lexical Analysis Error: {e}"
                error_trace = traceback.format_exc()
                error_tokens_text += "\n" + error_trace

        # Before returning the template, add this debug print
        print(f"Final error_semantic_text: {error_semantic_text}")  # Debug log
        
    return render_template(
        "index.html",
        code=code,
        result=result,
        error_tokens_text=error_tokens_text,
        error_syntax_text=error_syntax_text,
        error_semantic_text=error_semantic_text,  # Make sure this is passed
        output=output,
        identifier_count=identifier_count
)

if __name__ == "__main__":
    app.run(debug=True)