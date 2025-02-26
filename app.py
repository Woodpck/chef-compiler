from flask import Flask, render_template, request
from src.lexical.lexical import LexicalAnalyzer
from src.syntax.parser import Parser
from src.syntax.lexer import Lexer as syntLexer

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

    if request.method == "POST":
        code = normalize_newlines(request.form.get("code", ""))
        action = request.form.get("action")

        if action == "lexical" and code.strip():
            analyzer = LexicalAnalyzer()
            try:
                result = analyzer.tokenize(code)
                error_tokens_text = "\n".join(analyzer.errors)
            except Exception as e:
                error_tokens_text = f"An error occurred: {e}"

        elif action == "syntax" and code.strip():
            try:
                # Create a new lexer first
                lexer = syntLexer()
                
                # Create the Parser instance and pass both the lexer and code
                # This assumes your Parser class knows how to handle this
                parser = Parser(lexer=lexer)
                
                # Try to parse the code directly
                parse_result = parser.parse(code)
                
                # If parse was successful, prepare output
                if parse_result:
                    output = ["Syntax Analysis completed successfully"]
                    
                    # Format the parse result for display
                    if isinstance(parse_result, dict):
                        for key, value in parse_result.items():
                            output.append(f"{key}: {value}")
                    elif isinstance(parse_result, list):
                        output.extend([str(item) for item in parse_result])
                    else:
                        output.append(str(parse_result))
                
                # Check for syntax errors
                if hasattr(parser, 'errors') and parser.errors:
                    error_syntax_text = "\n".join([str(error) for error in parser.errors])
                elif not parse_result:
                    error_syntax_text = "Syntax analysis failed with no specific errors."
                
                 # ✅ Also get lexical tokens for syntax analysis
                analyzer = LexicalAnalyzer()
                try:
                    syntax_tokens = analyzer.tokenize(code)
                except Exception:
                    syntax_tokens = []
                
            except Exception as e:
                error_syntax_text = f"An error occurred during syntax analysis: {e}"
                output = [f"Syntax Analysis Error: {e}"]

    return render_template(
        "index.html",
        code=code,
        result=result,
        syntax_tokens=syntax_tokens,  # ✅ Correctly passing syntax tokens
        error_tokens_text=error_tokens_text,
        error_syntax_text=error_syntax_text,  # ✅ Ensuring this variable contains error messages
        output=output
    )

if __name__ == "__main__":
    app.run(debug=True)
