from flask import Flask, request, render_template, url_for, redirect
from flask.ext.markdown import Markdown

app = Flask(__name__)
Markdown(app)

def get_papers():
    return ["# Titre\n\nTexte", "## Titre 2\n\nTexte 2"]

@app.route('/')
def index():
    papers = get_papers()
    return render_template('index.html', papers=papers)

def main():
    app.run(host='0.0.0.0', debug=True)

if __name__ == "__main__":
    main()
