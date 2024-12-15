from flask import Flask, render_template, request
from src.lexical.lexical import LexicalAnalyzer

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = []
    error_tokens_text = ""
    error_syntax_text = ""
    error_semantic_text = ""
    code = ""
    
    if request.method == "POST":
        code = request.form.get("code", "")  # Get the input code from the form
        action = request.form.get("action", "")
        
        if action == "lexical":
            try:
                lexical_analyzer = LexicalAnalyzer()  # Create an instance of the Lexer class
                tokens, errors = lexical_analyzer.tokenize(code)  # Tokenize the code
                
                # The tokens are already in the correct format
                result = tokens
                
                # Convert errors to error messages
                if errors:
                    error_tokens_text = "\n".join(errors)
            except Exception as e:
                error_tokens_text = f"Lexical Analysis Error: {str(e)}"

    return render_template(
        "index.html",  # Render the HTML template
        result=result,
        code=code,  # Pass the original code back to the textarea
        error_tokens_text=error_tokens_text,
        error_syntax_text=error_syntax_text,
        error_semantic_text=error_semantic_text
    )

if __name__ == '__main__':
    app.run(debug=True)