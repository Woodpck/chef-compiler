from flask import Flask, render_template, request
from src.lexical.lexical import Lexer

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = []
    error_tokens_text = ""
    error_syntax_text = ""
    error_semantic_text = ""
    
    if request.method == "POST":
        code = request.form.get("code", "") 
        action = request.form.get("action", "")
        
        if action == "lexical":
            try:
                lexer = Lexer()
                tokens, errors = lexer.tokenize(code)  # Tokenize the code
                
                result = [(token[0], token[1]) for token in tokens]
                
                # error messages
                if errors:
                    error_tokens_text = "\n".join([error.as_string() for error in errors])
            except Exception as e:
                error_tokens_text = f"Lexical Analysis Error: {str(e)}"

    return render_template(
        "index.html",  
        result=result,
        error_tokens_text=error_tokens_text,
        error_syntax_text=error_syntax_text,
        error_semantic_text=error_semantic_text
    )

if __name__ == '__main__':
    app.run(debug=True)