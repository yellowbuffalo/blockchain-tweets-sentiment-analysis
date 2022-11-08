# Tweets Sentiment Analysis - Keyword: blockchain
The project for live update sentiment analysis on Twitter, using PySpark, Airflow, socket to build the project in CI/CD.
## Project Scheme:
  1. Using socket to get tweets(query:blockchain) from [Twitter API](https://developer.twitter.com/en/docs/twitter-api), and listen in port 5555.
  2. Implement PySpark to  connect data form port 5555, and conduct NLP dat processing and sentiment classify for tweets.
  3. Count the number for label: Positive, Negative, Neutral, and save the table to MongoDB.
  4. Read the data from MongoDB, and plot it by dash plotly. The result and plot will automatically update by the step1 and step2.
![Project Scheme](https://github.com/yellowbuffalo/blockchain-tweets-sentiment-analysis/blob/main/img/process.JPG?raw=true)
