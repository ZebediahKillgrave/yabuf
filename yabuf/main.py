from flask import Flask, request, render_template, session, url_for, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def main():
    app.run(host='0.0.0.0', debug=True)

if __name__ == "__main__":
    main()
