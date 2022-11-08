# Tweets Sentiment Analysis - Keyword: blockchain - Live Update
The project for live update sentiment analysis on Twitter, using PySpark, Airflow, MongoDB, socket to build the project in CI/CD.
## Demo Video:
[![Watch the video](https://img.youtube.com/vi/p2HIDqMh2jQ/0.jpg)](https://youtu.be/p2HIDqMh2jQ)
## Project Scheme:
  1. Using socket to get tweets(query:blockchain) from [Twitter API](https://developer.twitter.com/en/docs/twitter-api), and listen in port 5555.
  2. Implement PySpark to  connect data form port 5555, and conduct NLP dat processing and sentiment classify for tweets.
  3. Count the number for label: Positive, Negative, Neutral, and save the table to MongoDB.
  4. Read the data from MongoDB, and plot it by dash plotly. The result and plot will automatically update by the step1 and step2.

![Project Scheme](https://github.com/yellowbuffalo/blockchain-tweets-sentiment-analysis/blob/main/img/process.JPG?raw=true)

## Install and Usage:
*  First, you should apply for the Twitter development account on [Twitter API](https://developer.twitter.com/en/docs/twitter-api).
  ```python
  
consumer_key = 'XXXXXXXXXXXXXXXXXXX'
consumer_secret = 'XXXXXXXXXXXXXXXXXXX'
access_token = 'XXXXXXXXXXXXXXXXXXX'
access_secret = 'XXXXXXXXXXXXXXXXXXX'
  ```
*  Then, Using following to build environment:
  ```console
  user@bar:~$ python3 -m venv myenv
  user@bar:~$ source myenv/bin/activate
  user@bar:~$ pip3 install -r requirements.txt
  ```
*  For airflow, there are some code should be conducted first:
  ```console
  user@bar:~$ mkdir ~/airflow
  user@bar:~$ export AIRFLOW_HOME=~/airflow
  user@bar:~$ airflow db init
  ```
*  And put the dags and etc files into "airflow" file as the structure below:
![structure](https://github.com/yellowbuffalo/blockchain-tweets-sentiment-analysis/blob/main/img/tree.png?raw=true)

*  Running the code below to start the Airflow session:
  ```console
  user@bar:~$ airflow webserver -p 8080
  ```
*  Open another terminal to start the schedule:
  ```console
  user@bar:~$ airflow scheduler
  ```
*  Then, http://localhost:8080 will show the task, running and start the task
![Airflow](https://github.com/yellowbuffalo/blockchain-tweets-sentiment-analysis/blob/main/img/airflow.png?raw=true)
![graph](https://github.com/yellowbuffalo/blockchain-tweets-sentiment-analysis/blob/main/img/airflow_graph.png?raw=true)

*  The task will start!

## Note:
Can also run the code below by using 3 terminal:
  ```console
  user@bar:~$ python3 {{script path}}/tweet_sender.py
  ```
  ```console
  user@bar:~$ python3 {{script path}}/tweets_connect.py
  ```
  ```console
  user@bar:~$ python3 {{script path}}/app.py
  ```
