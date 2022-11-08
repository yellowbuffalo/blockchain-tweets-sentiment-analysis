'''
The script is to getting the data from twitter api, and using socket 
to listening the data in port 5555 localhost.
'''
import tweepy
from tweepy.auth import OAuthHandler
from tweepy import Stream
import socket
import json

# request to get credentials at http://developer.twitter.com
consumer_key = 'XXXXXXXXXXXXXXXXXXX'
consumer_secret = 'XXXXXXXXXXXXXXXXXXX'
access_token = 'XXXXXXXXXXXXXXXXXXX'
access_secret = 'XXXXXXXXXXXXXXXXXXX'
'''
The class is to listening the tweets from streaming.
'''
class TweetsListener(Stream):

    def __init__(self, *args, csocket):
        super().__init__(*args)
        self.client_socket = csocket
    # we override the on_data() function in StreamListener
    def on_data(self, data):
        try:
            message = json.loads( data )
            print( message['text'].encode('utf-8') )
            self.client_socket.send((str(message['text']) + "\n").encode('utf-8'))
            return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def if_error(self, status):
        print(status)
        return True

# Search and get the tweets related the keyword "blackchain".
def send_tweets(c_socket):
    print('start sending data from Twitter to socket')
    twtr_stream = TweetsListener(
        consumer_key, consumer_secret,
        access_token, access_secret,
        csocket=c_socket
    )
    twtr_stream.filter(track=['blockchain'], languages=["en"])



if __name__ == "__main__":
    new_skt = socket.socket()         # initiate a socket object
    host = "127.0.0.1"     # local machine address
    port = 5555                 # specific port for your service.
    new_skt.bind((host, port))        # Binding host and port

    print("Now listening on port: %s" % str(port))

    new_skt.listen(5)                 #  waiting for client connection.
    c, addr = new_skt.accept()        # Establish connection with client. it returns first a socket object,c, and the address bound to the socket

    print("Received request from: " + str(addr))
    # and after accepting the connection, send the tweets through the socket
    send_tweets(c)