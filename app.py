from flask import Flask, render_template, request
from src.lexical.lexical import LexicalAnalyzer
from src.syntax.syntax import LL1Parser, cfg, parse_table, follow_set

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
    code = ""
    output = []  # Stores syntax analysis output
    identifier_count = 0  # Initialize identifier count
    
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
                    
                    # If parse was successful, prepare output
                    if success:
                        output = ["Syntax Analysis completed successfully"]
                        output.append("Parse Tree:")
                        output.append(str(parser.parse_tree)) 
                    
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

    return render_template(
        "index.html",
        code=code,
        result=result,
        syntax_tokens=syntax_tokens,
        error_tokens_text=error_tokens_text,
        error_syntax_text=error_syntax_text,
        output=output,
        identifier_count=identifier_count
    )

if __name__ == "__main__":
    app.run(debug=True)