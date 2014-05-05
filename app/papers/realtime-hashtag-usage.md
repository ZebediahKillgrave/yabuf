title : Realtime chart showing hashtag usage

date : 04-02-2014

description : In this post I will explain how I made a realtime graph comparing two hashtags usage with Python, javascript and websockets.

author : volent

----------

I recently started to use the [tweepy](https://github.com/tweepy/tweepy) module for work and used the API a lot. Unfortunately I didn't find any opportunity to use the stream part of the API, so after some thinking I went with the idea that following **hashtag usage in realtime** would be awesome !

> If you want to try this at home, get some API keys at dev.twitter.com

### Get the twitter stream

The first part of the project is all about getting the stream containing tweets with the hashtags we want to track.

Let's first try to get the tweet stream with a unique hashtag.

>     pip install tweepy

    :::python
    # /stream.py
    import tweepy
    
    CONSUMER_KEY, CONSUMER_SECRET = '', '' # dev.twitter.com to get yours
    USER_KEY, USER_SECRET = '', ''  	   # same here
    
    class MyStream(tweepy.StreamListener):
        def __init__(self):
            tweepy.StreamListener.__init__(self)
            
        def on_status(self, tweet):
            print tweet.text
    
    def main():
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(USER_KEY, USER_SECRET)
        stream = tweepy.Stream(auth, MyStream(), timeout=50)
        stream.filter(track=["#science"])
        
    if __name__ == "__main__":
        main()

Should we try it ?

    :::shell
    $ python stream.py
    Don't Stop Drinking Water http://bit.ly/1j0I29I  #Water #Science
    ...

Wow, that was easy ! Let's track two hashtags now :

    	 stream.filter(track=["#science", "#football"])

Tweepy is definitely awesome ! 
    
We now need to know which tweet is containing one, the other or both hashtags. Don't worry, no need to parse anything or use any kind of regular expression, Twitter is kind enough to parse this for us and we can easily access this data using tweepy :

    :::python
        def on_status(self, tweet):
    	    hashtags = [hashtag["text"] for hashtag in tweet.entities["hashtags"]]
            # hashtag["text"] does not contain the starting '#'
            if "science" in hashtags:
               print "This tweet is about #science !"
            if "football" in hashtags:
               print "This tweet is about #football !"
            
This is starting to be interesting, we are now getting the amount of tweet for each hashtag. But in order to send it later to our webapp, we will publish new status on a redis channel. This way we will be able to subscribe to the channel on the webapp and keep track of incoming status.

> You need redis-server and the python redis library for the next step
>
>     apt-get install redis-server
>     pip install redis
>

    :::python
    import redis

    redis = redis.Redis('localhost')

    class MyStream(tweepy.StreamListener):
    	  def __init__(self):
              tweepy.StreamListener.__init__(self)

          def on_status(self, tweet):
              hashtags = [hashtag["text"] for hashtag in tweet.entities["hashtags"]]
              # hashtag["text"] does not contain the starting '#'
              if "science" in hashtags:
              	 redis.publish("hashtag", "science")
              if "football" in hashtags:
              	 redis.publish("hashtag", "football")

We are now done with the twitter stream !

### Display the chart

The second part is about displaying the chart. To do this, I will use [smoothie.js](https://github.com/joewalnes/smoothie/), [Flask](https://github.com/mitsuhiko/flask) and [Flask-Sockets](https://github.com/kennethreitz/flask-sockets).

>     pip install flask
>     pip install flask-sockets

We will first create the simple flask app that will serve our html page.

    :::python
    from flask import Flask, render_template
    
    app = Flask(__name__)
    
    @app.route('/')
    def index():
    	return render_template('index.html')

    if __name__ == "__main__":
        app.run()

With a simple template :

    :::html
    <html>
      <head>
        <title>Realtime hashtag usage chart</title>
        <script type="text/javascript" src="{{ url_for('static', filename='smoothie.js') }}"></script>
        <script type="text/javascript">
          function createTimeline() {
            var chart = new SmoothieChart();
            chart.streamTo(document.getElementById("chart"), 500);
          }
        </script>
      </head>
      <body onload="createTimeline()">
        <canvas id="chart" width="800" height="300"></canvas>
      </body>
    </html>

Don't forget the folder structure needed for a flask project :

    /
    |- app.py
    |
    |- static/
    |    |- smoothie.js
    |
    |- templates/
         |- index.html


Take a look at our beautiful empty chart at 127.0.0.1:5000 !

There are still two things to do : get the data sent by our tweepy backend and send it to the client's browser.

The first part will be using gevent to fetch the data asyncronously and I've been stuck quite a while on this. I still don't know if it's the way to go so please feel free to leave a comment if I'm not doing it the right way.

    :::python
    import gevent.monkey
    gevent.monkey.patch_all() # This is the part i'm not sure about

    from flask import Flask, render_template
    import redis
    import gevent

    app = Flask(__name__)
    redis = redis.Redis('localhost')

    class Updater(object):
        def __init__(self, redis):
            self.redis = redis
            self.pubsub = redis.pubsub()
            self.pubsub.subscribe("hashtag")

    	def run(self):
            for data in (data for data in self.pubsub.listen()):
            	print data

    	def start(self):
            gevent.spawn(self.run)

    updater = Updater(redis).start()

    @app.route('/')
    def index():
    	return render_template('index.html')

    if __name__ == "__main__":
       app.run()

If you launch this and the python script we wrote in the first part, you should have an output like this :

    :::shell
    * Running on http://127.0.0.1:5001/
    {'pattern': None, 'type': 'subscribe', 'channel': 'hashtag', 'data': 1L}
    {'pattern': None, 'type': 'message', 'channel': 'hashtag', 'data': 'science'}
    {'pattern': None, 'type': 'message', 'channel': 'hashtag', 'data': 'football'}

And that's great because it means we are getting the data we want to display !
The last step is about sending the data to the client and displaying it. This is where we'll use websockets. 

I've never done Websockets but hey, I'm pretty good at raw sockets so that should be easy ! Well, I still got stucked for a little while before understanding exactly how it works. But I think I got it now and I came to this code :

    :::javascript
    function createTimeline() {
      var chart = new SmoothieChart();
      chart.streamTo(document.getElementById("chart"), 500);

      var inbox = new WebSocket("ws://127.0.0.1:8000/hashtag");

      inbox.onmessage = function(message) {
        console.log(message.data);
      }
    }

That was for the `index.html` file. We will only log the data we get for now. It's a little more complicated for the server part and there is one thing you should know before trying to launch the webserver using `app.run()`. 

Flask uses WSGI as a default server and WSGI does not support websockets, so we will use `gunicorn`. You can already try it with `gunicorn -k flask_sockets.worker app:app`. This should launch the web server and display the empty chart exactly like before but on the port 8000. You can use `-b 127.0.0.1:5000` if you want to use the port 5000, though.

I'll paste the whole new version of `app.py` because there is a lot a new code and it will be the final version.

    :::python
    import gevent.monkey
    gevent.monkey.patch_all()

    from flask import Flask, render_template
    from flask_sockets import Sockets
    import redis
    import gevent

    app = Flask(__name__)
    redis = redis.Redis('localhost')
    sockets = Sockets(app)

    class Updater(object):
        def __init__(self, redis):
            self.clients = []
            self.redis = redis
            self.pubsub = redis.pubsub()
            self.pubsub.subscribe("hashtag")

	def send(self, client, data):
            try:
                client.send(str(data['data']))
            except:
                self.clients.remove(client)
    
        def run(self):
            for data in (data for data in self.pubsub.listen()):
                for client in self.clients:
                    gevent.spawn(self.send, client, data)

        def start(self):
            gevent.spawn(self.run)

    updater = Updater(redis)

    updater.start()

    @sockets.route('/hashtag')
    def hashtag(ws):
        updater.clients.append(ws)
        while True: gevent.sleep(1)

    @app.route('/')
    def index():
        return render_template('index.html')


That works great, we can see in our browser when twitter sends us a science or football hashtag !
Final step to make everything work : draw that empty chart ! There is not that much difficulty here since `smoothie.js` is really easy to use, so even if I'm not really good at javascript, I should be able to do it.

    :::javascript
    function createTimeline() {
	var science = new TimeSeries();
	var football = new TimeSeries();
	var chart = new SmoothieChart({
	    millisPerPixel: 200,
	    grid : {
		lineWidth: 0.5,
		millisPerLine: 5000,
		verticalSections: 2
	    }
	});
	chart.streamTo(document.getElementById("chart"), 200);

	chart.addTimeSeries(football, {
	    strokeStyle: 'rgba(0, 255, 0, 1)', 
	    fillStyle: 'rgba(0, 255, 0, 0.2)'
	});
	chart.addTimeSeries(science, {
	    strokeStyle: 'rgba(255, 0, 0, 1)', 
	    fillStyle: 'rgba(255, 0, 0, 0.2)'
	});
	
	var inbox = new WebSocket("ws://127.0.0.1:8000/hashtag");

	var nScience = 0;
	var nFootball = 0;

	inbox.onmessage = function(message) {
	    if (message.data == "science") {
		nScience += 1;
		science.append(new Date().getTime(), nScience);
	    }
	    else if (message.data == "football") {
		nFootball += 1;
		football.append(new Date().getTime(), nFootball);
	    }
	}
    }

Yay ! Done ! That looks nice and science & football are really good competitors, they stay really close to each other (science is red & football is green).

#### Result

<img src="/static/img/example-chart.png" alt="example chart" width=650 />

Thanks a lot if you've read this far, let me know if this was too long, cool, boring or whatever, I'll gladly correct any typo or error I made.

I think the next post will be a lot shorter, and I'll try to write about something else than python/javascript.