from flask import Flask, render_template, request
from src.lexical.lexical import LexicalAnalyzer

app = Flask(__name__)

def normalize_newlines(text):
    """Normalize newline characters for cross-platform compatibility."""
    return text.replace("\r\n", "\n").replace("\r", "\n")

@app.route("/", methods=["GET", "POST"])
def index():
    result = []
    error_tokens_text = ""
    code = ""

    if request.method == "POST":
        code = normalize_newlines(request.form.get("code", ""))
        action = request.form.get("action")

        if action == "lexical" and code.strip():
            analyzer = LexicalAnalyzer()
            try:
                tokens = analyzer.tokenize(code)
                result = tokens
                error_tokens_text = "\n".join(analyzer.errors)
            except Exception as e:
                error_tokens_text = f"An error occurred: {e}"

    return render_template(
        "index.html",
        code=code,
        result=result,
        error_tokens_text=error_tokens_text,
        error_syntax_text="Feature coming soon!"
    )

if __name__ == "__main__":
    app.run(debug=True)