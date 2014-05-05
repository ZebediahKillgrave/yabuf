from flask import Flask, request, render_template, url_for, redirect, abort
from werkzeug.contrib.atom import AtomFeed
from urlparse import urljoin
from markdown import markdown
from os import listdir, stat
from os.path import isfile, join, dirname
from time import asctime, gmtime
from datetime import datetime

app = Flask(__name__)
PAPERS_PATH = join(dirname(__file__), 'papers/')

class HeaderGrammar(object):

    """
    Parse header grammar.
    For each variable it will setattr(self, variable, value).
    """

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
    def __init__(self, raw, paper_name=""):
        self.raw = raw
        hg = HeaderGrammar(raw)
        hg.parse()

        date = getattr(hg, "date", "01-01-2000")
        self.date = datetime.strptime(date, "%m-%d-%Y")
        self.paper_name = paper_name
        self.fmt_date = datetime.strftime(self.date, "%A, %d %B %Y")
        self.author = getattr(hg, "author", "volent")
        self.title = getattr(hg, "title", paper_name)
        self.sticky = getattr(hg, "sticky", None)
        self.description = getattr(hg, "description", None)
        self.content = markdown(hg.content, output_format="html5", extensions=['codehilite'])

def fetch_all_papers():
    papers = []
    stickies = []

    # http://stackoverflow.com/a/3207973/2437219
    paper_files = (f for f in listdir(PAPERS_PATH)
                   if (isfile(join(PAPERS_PATH, f))))

    for paper_file in paper_files:
        file_path = join(PAPERS_PATH, paper_file)
        with open(file_path) as f:
            paper_name = paper_file.split('.')[0]
            paper = Paper(f.read(), paper_name)
            papers.append((paper.date, paper))
            if paper.sticky:
                stickies.append((paper_name, paper.sticky))
    return stickies, papers

@app.route('/<paper_name>')
def papers(paper_name):
    stickies, papers = fetch_all_papers()
    try:
        paper = [p[1] for p in papers if p[1].paper_name == paper_name][0]
    except IndexError:
        return abort(404)
    return render_template("paper.html", paper_name=paper_name, stickies=stickies, paper=paper)

@app.route('/')
def index():
    stickies, papers = fetch_all_papers()
    papers.sort()
    papers = [p[1] for p in papers if not p[1].sticky]
    papers.reverse()
    stickies.sort()
    return render_template('index.html', paper_name='index', # don't remove
                           stickies=stickies, papers=papers)

def make_external(url):
    return urljoin(request.url_root, url)

@app.route('/recent.atom')
def recent_feed():
    stickies, papers = fetch_all_papers()
    papers.sort()
    papers = [p[1] for p in papers if not p[1].sticky]
    papers.reverse()

    feed = AtomFeed('blog.volent.fr - Recent Articles',
                    feed_url=request.url, url=request.url_root)

    for article in papers[:15]:
        feed.add(article.title, unicode(article.content),
                 content_type='html',
                 author=article.author,
                 url=make_external(article.paper_name),
                 updated=article.date,
                 published=article.date)
    return feed.get_response()

def main():
    app.run(host='0.0.0.0', debug=True)

if __name__ == "__main__":
    main()
