title : Realtime graph showing hashtag usage

date : 04-02-2014

----------

I recently started to use the [tweepy](https://github.com/tweepy/tweepy) module for work and used the API a lot. Unfortunately I didn't find any opportunity to use the stream part of the API, so after some thinking I went with the idea that following **hashtag usage in realtime** would be awesome !

> If you want to try this at home, get some API keys at dev.twitter.com

### Get the twitter stream

The first part of the project is all about getting that twitter stream. We need something that with a hashtags list will give us the tweet number for each hashtag during a given period.

We will start with getting the tweet stream with a unique hashtag.

> Don't forget to `pip install tweepy` 

    import tweepy
    
    CONSUMER_KEY, CONSUMER_SECRET = '', '' # fill with yours
    USER_KEY, USER_SECRET = '', ''         # same here
    
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

You can then launch the little script we wrote and enjoy a coffee while reading tweets about science.

Now that we've got this done it's really easy to track more than one hashtag, as you've probably already seen the `track` parameter is a list so we just have to add the hashtag we want to the list :

    	 stream.filter(track=["#science", "#football"])
    
But we also need to know if a status if containing one, the other or both hashtags. Don't worry, no need to parse anything or use any king of regular expression, Twitter is kind enough the parse this for us and we can access this data easily using tweepy :

        def on_status(self, tweet):
    	    hashtags = [hashtag["text"] for hashtag in tweet.entities["hashtags"]]
            # hashtag["text"] does not contain the starting '#'
            if "science" in hashtags:
               print "This tweet is about #science !"
            if "football" in hashtags:
               print "This tweet is about #football !"
            
That is starting to be interesting, we can now easily get the tweet number about each subject.