from flask import Flask, request, render_template, url_for, redirect, abort
from markdown import markdown
from os import listdir
from os.path import isfile, join, dirname

app = Flask(__name__)
PAPERS_PATH = join(dirname(__file__), 'papers/')

class HeaderGrammar(object):

    expr_sep = ":"
    expr_comment = "//"
    expr_eoh = "----------"

    def __init__(self, raw):
        self.raw = raw
        self.content = ""

    def parse(self):
        lines = self.raw.split('\n')
        for i, line in enumerate(lines):
            if line == self.expr_eoh:
                self.content = '\n'.join(lines[i + 1:])
                break

            comment_index = line.find(self.expr_comment)
            if comment_index != -1:
                line = line[:comment_index]

            sep_index = line.find(self.expr_sep)
            if sep_index != -1:
                setattr(self, line[:sep_index].strip(), line[sep_index + 1:].strip())

        else:
            self.content = self.raw

class Paper(object):
    def __init__(self, raw, title=""):
        self.raw = raw
        hg = HeaderGrammar(raw)
        hg.parse()

        self.created_at = getattr(hg, "created_at", "Unknown")
        self.author = getattr(hg, "author", "volent")
        self.title = getattr(hg, "title", title)
        self.content = markdown(hg.content, output_format="html5", extensions=['codehilite'])

def fetch_all_papers():
    papers = {}

    # http://stackoverflow.com/a/3207973/2437219
    paper_files = (f for f in listdir(PAPERS_PATH)
                   if (isfile(join(PAPERS_PATH, f))))

    for paper_file in paper_files:
        with open(join(PAPERS_PATH, paper_file)) as f:
            papers[paper_file.split('.')[0]] = Paper(f.read(), paper_file)

    return papers

@app.route('/<paper_name>')
def papers(paper_name):
    papers = fetch_all_papers()
    try:
        paper = papers[paper_name]
    except KeyError:
        return abort(404)
    if paper_name == "contact":
        return render_template("contact.html", content=paper)
    elif paper_name == "about":
        return render_template("about.html", content=paper)
    return render_template("paper.html", content=paper)

@app.route('/')
def index():
    papers = fetch_all_papers()
    papers = {paper_name:papers[paper_name] for paper_name in papers
              if paper_name != "about" and paper_name != "contact"}
    return render_template('index.html', papers=papers)

def main():
    app.run(host='0.0.0.0', debug=True)

if __name__ == "__main__":
    main()
