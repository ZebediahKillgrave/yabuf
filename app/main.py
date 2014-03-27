from flask import Flask, request, render_template, session, url_for, redirect, flash
import redis

app = Flask(__name__)
app.secret_key = "secret"
redis = redis.Redis('localhost')

def logged_in(login = None):
    if login is not None:
        session["login"] = login
    try:
        login = session["login"]
    except KeyError:
        session["login"] = False
        return False
    return login

@app.route('/post', methods=['POST'])
def post():
    if 'content' in request.values and logged_in():
        redis.rpush("content", request.values['content'])
        flash("Post sucess.", 'success')
    else:
        flash("Post failed.", 'error')
    return redirect(url_for('index'))
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if logged_in():
        return redirect(url_for('index'))
    elif 'user' in request.values and 'password' in request.values:
        if not redis.get("user") or not redis.get("password"):
            redis.set("user", request.values['user'])
            redis.set("password", request.values['password'])
            flash("Registration success.", 'success')
            logged_in(True)
            return redirect(url_for('index'))
        elif (redis.get("user") == request.values['user'] and
            redis.get("password") == request.values['password']):
            logged_in(True)
            flash("Authentication success.", 'success')
            return redirect(url_for('index'))
        else:
            flash("Authentication failed.", 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    logged_in(False)
    flash("Logout success.", 'success')
    return redirect(url_for('index'))

@app.route('/')
def index():
    content = (post.decode('utf-8') for post in redis.lrange("content", 0, -1))
    return render_template('index.html', content=content, login=logged_in())

def main():
    app.run(host='0.0.0.0', debug=True)

if __name__ == "__main__":
    main()
