# Tweets Sentiment Analysis - Keyword: blockchain
The project for live update sentiment analysis on Twitter, using PySpark, Airflow, socket to build the project in CI/CD.
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
*  Then, http://localhost:8080 will show the task, running and start the task <span style="color:orange;">Word up</span>
