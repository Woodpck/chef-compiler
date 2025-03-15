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
                                    
                                    # Debug - print what we received from semantic analyzer
                                    print(f"DEBUG - Semantic analysis result: success={semantic_success}")
                                    print(f"DEBUG - Semantic messages: {semantic_messages}")
                                    
                                    if semantic_success:
                                        # Use the output_messages from semantic analyzer
                                        output = semantic_analyzer.output_messages
                                        if not output:  # If no specific messages, add a default one
                                            output = ["Semantic analysis completed successfully!"]
                                    else:
                                        # FIXED: Use returned messages for errors instead of accessing analyzer.errors
                                        error_semantic_text = "\n".join(semantic_messages)
                                        # Still show any available output messages even if there were errors
                                        output = semantic_analyzer.output_messages
                                    
                                    # Debug - print what we're passing to the template
                                    print(f"DEBUG - error_semantic_text: {error_semantic_text}")
                                    print(f"DEBUG - output: {output}")
                                
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
    
    # Debug - final check of what we're sending to template
    if error_semantic_text:
        print(f"DEBUG - Final error_semantic_text: {error_semantic_text}")
    
    return render_template(
        "index.html",
        code=code,
        result=result,
        error_tokens_text=error_tokens_text,
        error_syntax_text=error_syntax_text,
        error_semantic_text=error_semantic_text,  # Make sure this is passed to template
        output=output,
        identifier_count=identifier_count
    )

# Add a test route to verify error display
@app.route("/test_semantic_error")
def test_semantic_error():
    # Simulate a semantic error
    error_semantic_text = "Test semantic error: Function 'test' missing return statement"
    output = ["Semantic analysis detected issues"]
    code = "dinein\nfunction pasta test()\n{\n}\ntakeout"
    
    return render_template(
        "index.html",
        code=code,
        result=[],
        error_tokens_text="",
        error_syntax_text="",
        error_semantic_text=error_semantic_text,
        output=output,
        identifier_count=0
    )

if __name__ == "__main__":
    app.run(debug=True)