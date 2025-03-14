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
        elif action == "syntax" and code.strip():
            analyzer = LexicalAnalyzer()
            try:
                lexical_tokens = analyzer.tokenize(code)
                identifier_count = analyzer.identifier_count  # Get the count
                error_tokens_text = "\n".join(analyzer.errors) if hasattr(analyzer, 'errors') else ""
                
                if error_tokens_text:
                    result = lexical_tokens
                    error_syntax_text = "Cannot proceed with Syntax Analysis due to Lexical Errors"
                else:
                    syntax_tokens = []
                    for i, (lexeme, token) in enumerate(lexical_tokens, 1):
                        syntax_tokens.append((lexeme, token, i))
                    
                    # Store the original tokens for display
                    result = lexical_tokens
                    
                    # Create the Parser instance with required parameters
                    parser = LL1Parser(cfg, parse_table, follow_set)
                    
                    # Parse using the tokens from lexical analysis
                    success, errors = parser.parse(syntax_tokens)
                    
                    # Check for syntax errors
                    if errors:
                        error_syntax_text = "\n".join(errors)
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
                error_tokens_text = "\n".join(analyzer.errors) if hasattr(analyzer, 'errors') else ""
                
                if error_tokens_text:
                    result = lexical_tokens
                    error_semantic_text = "Cannot proceed with Semantic Analysis due to Lexical Errors"
                else:
                    # Run syntax analysis
                    syntax_tokens = []
                    for i, (lexeme, token) in enumerate(lexical_tokens, 1):
                        syntax_tokens.append((lexeme, token, i))
                    
                    # Store the original tokens for display
                    result = lexical_tokens
                    
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
                            # Debug information for parse tree
                            print("Parse Tree before Semantic Analysis:")
                            print(parser.parse_tree)
                            
                            # Create semantic analyzer instance
                            semantic_analyzer = SemanticAnalyzer()
                            
                            # Check if parse tree exists
                            if not parser.parse_tree:
                                error_semantic_text = "Parse tree not available for semantic analysis"
                                output = ["Semantic analysis failed: No parse tree available"]
                            else:
                                # Run semantic analysis with parse tree
                                semantic_success, semantic_messages = semantic_analyzer.analyze(parser.parse_tree)
                                
                                if semantic_success:
                                    # Use the output_messages from semantic analyzer
                                    output = semantic_analyzer.output_messages
                                    if not output:  # If no specific messages, add a default one
                                        output = ["Semantic analysis completed successfully!"]
                                else:
                                    # Set semantic errors string
                                    error_semantic_text = "\n".join(semantic_analyzer.errors)
                                    # Still show any available output messages even if there were errors
                                    output = semantic_analyzer.output_messages
                            
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
    
    return render_template(
        "index.html",
        code=code,
        result=result,
        error_tokens_text=error_tokens_text,
        error_syntax_text=error_syntax_text,
        error_semantic_text=error_semantic_text,  # Pass semantic errors to template
        output=output,
        identifier_count=identifier_count
    )

if __name__ == "__main__":
    app.run(debug=True)