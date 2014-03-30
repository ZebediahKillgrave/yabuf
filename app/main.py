from flask import Flask, request, render_template, url_for, redirect, abort
from markdown import markdown
from os import listdir, stat
from os.path import isfile, join, dirname
from time import asctime, gmtime

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

        self.created_at = getattr(hg, "created_at", "Unkown")
        self.author = getattr(hg, "author", "volent")
        self.title = getattr(hg, "title", title)
        self.sticky = getattr(hg, "sticky", None)
        self.content = markdown(hg.content, output_format="html5", extensions=['codehilite'])

def fetch_all_papers():
    papers = {}
    stickies = []

    # http://stackoverflow.com/a/3207973/2437219
    paper_files = (f for f in listdir(PAPERS_PATH)
                   if (isfile(join(PAPERS_PATH, f))))

    for paper_file in paper_files:
        file_path = join(PAPERS_PATH, paper_file)
        with open(file_path) as f:
            paper_name = paper_file.split('.')[0]
            paper = Paper(f.read(), paper_file)
            papers[paper_name] = paper
            if paper.sticky:
                stickies.append((paper_name, paper.sticky))

    return stickies, papers

@app.route('/<paper_name>')
def papers(paper_name):
    stickies, papers = fetch_all_papers()
    try:
        paper = papers[paper_name]
    except KeyError:
        return abort(404)
    return render_template("paper.html", paper_name=paper_name, stickies=stickies, content=paper)

@app.route('/')
def index():
    stickies, papers = fetch_all_papers()
    papers = {paper_name:papers[paper_name] for paper_name in papers
              if paper_name not in (s[0] for s in stickies)}
    return render_template('index.html', paper_name='index', stickies=stickies, papers=papers)

def main():
    app.run(host='0.0.0.0', debug=True)

if __name__ == "__main__":
    main()
