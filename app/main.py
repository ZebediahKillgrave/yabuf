from flask import Flask, request, render_template, url_for, redirect
from markdown import markdown
from os import listdir
from os.path import isfile, join

app = Flask(__name__)
PAPERS_PATH = 'papers/'

def get_papers():
    papers = []
    
    # http://stackoverflow.com/a/3207973/2437219
    paper_files = (f for f in listdir(PAPERS_PATH)
                   if (isfile(join(PAPERS_PATH, f)) and
                       f.endswith(".release")))

    for paper_file in paper_files:
        with open(join(PAPERS_PATH, paper_file)) as f:
            papers.append(markdown(f.read(), 
                                   output_format="html5",
                                   extensions=['codehilite']))

    return papers

@app.route('/')
def index():
    papers = get_papers()
    return render_template('index.html', papers=papers)

def main():
    app.run(host='0.0.0.0', debug=True)

if __name__ == "__main__":
    main()
