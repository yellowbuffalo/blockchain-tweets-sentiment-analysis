'''
The script is to connect the tweets data from port 5555 in "tweet_sender.py".
Doing the data processing and using Textblob's sentiment classify to detect
the sentiment label for every tweet, finally, save the result to the mongodb
by PySpark.
'''
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import SQLContext,SparkSession
from pyspark.sql.functions import desc
from collections import namedtuple
from textblob import TextBlob
import pymongo
import time

# Sentiment analysis for the tweet
def sentiment_classify(sentence):
    value = TextBlob(sentence).sentiment.polarity
    if value >= 0.6: # Positive if the value > 0.6
        return 'Positive'
    elif value <= 0.4: # Positive if the value < 0.4
        return 'Negative'
    else: # Others, Neutral
        return 'Neutral'

if __name__ == "__main__":
    sc = SparkContext() # Open a spark project
    ssc = StreamingContext(sc, 10 )
    sqlContext = SQLContext(sc)
    socket_stream = ssc.socketTextStream("127.0.0.1", 5555) # Get the tweets form port 5555.

    lines = socket_stream.window( 20 )
    fields = ("tag", "count" )
    Tweet = namedtuple( 'Tweet', fields )
    # Conduct the RDD method to processing the data.
    ( lines.flatMap( lambda text: [sentiment_classify(text)] )  # Sentiment analysis.
                 .map( lambda word: ( word, 1 ) ) 
                 .reduceByKey( lambda a, b: a + b ) 
                 .map( lambda rec: Tweet( rec[0], rec[1] ) ) 
                 .foreachRDD( lambda rdd: rdd.toDF().sort("count")      
                 .limit(10).createOrReplaceTempView("tweets") ) ) 
    # Start the task.
    ssc.start()
    while True:
        try:
            time.sleep( 10 ) # Sleep 10s.
            sentiment_tweets = sqlContext.sql( 'Select * from tweets' ) # Loading tweets from temp sql.
            #     top_10_tweets.createOrReplaceTempView("tweets")
            sentiment_tweets.show()
            sentiment_tweets = sentiment_tweets.toPandas() # Change the table to pandas dataframe.

            myclient = pymongo.MongoClient("mongodb://localhost:27017/") # Connect to mongodb.
            database = myclient["twitter_db"]  # SQL: Database Name
            collist = database.list_collection_names()
            records = sentiment_tweets.to_dict('records')
            collection = database["sentiment"] # Setting the collection name.
            collection.delete_many({})
            collection.insert_many(records) # Insert the data.
        except:
            print('No data yet.')