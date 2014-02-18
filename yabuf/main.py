from flask import Flask, request, render_template, session, url_for, redirect
import redis

app = Flask(__name__)
redis = redis.Redis('localhost')

@app.route('/post', methods=['POST'])
def post():
    if 'content' in request.values:
        redis.rpush("content", request.values['content'])
    return redirect(url_for('index'))
    

@app.route('/')
def index():
    content = (post.decode('utf-8') for post in redis.lrange("content", 0, -1))
    return render_template('index.html', content=content)

def main():
    app.run(host='0.0.0.0', debug=True)

if __name__ == "__main__":
    main()
