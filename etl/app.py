'''
The script is for live update dash app.
'''
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly_express as px
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import Row
from collections import deque
from threading import Thread

# Using Spark session to get tweet sentiment data from mongodb.
spark = SparkSession \
.builder \
.appName("mongodbtest1") \
.master('local')\
.config("spark.mongodb.input.uri", "mongodb://localhost:27017/twitter_db.sentiment") \
.config("spark.mongodb.output.uri", "mongodb://localhost:27017/twitter_db.sentiment") \
.config('spark.jars.packages', 'org.mongodb.spark:mongo-spark-connector_2.12:3.0.1') \
.getOrCreate()

data = spark.read\
.format('com.mongodb.spark.sql.DefaultSource')\
.option( "uri", "mongodb://localhost:27017/twitter_db.sentiment") \
.load()

# Setting the update function for visualization.
q = deque()
q.append(data)
def read_stream(q): # Update the data by loading new data from mongodb.
    data = spark.read\
    .format('com.mongodb.spark.sql.DefaultSource')\
    .option( "uri", "mongodb://localhost:27017/twitter_db.sentiment") \
    .load()
    q.popleft()
    q.append(data) # record the latest data by queue.
x = Thread(target=read_stream, args=(q,))
x.start()

df = q[0].toPandas()

# Design the chart for tweets sentiment analysis.
palette = {"Negative": "#9F353A","Neutral":"#D7C4BB", "Positive": "#86C166"}
fig = px.pie(df, values='count', names='tag', color='tag',
             title='Sentiment Distribution on Twitter\nKeyword: blockchain',
            color_discrete_map = palette)
# Open a dash app.
app = dash.Dash(__name__)
# Design the app layout.
app.layout = html.Div(
 children = [
     dcc.Graph(
         figure = fig, id="live-update-graph"),
     dcc.Interval(
            id="interval-component", interval=1 * 1000, n_intervals=0  # in milliseconds
        ),
])

# Usong chart's id to update the new chart.
@app.callback(
    Output("live-update-graph", "figure"), 
    Input("interval-component", "n_intervals")
)
def update_graph(n):
    df = q[0].toPandas()

    palette = {"Negative": "#9F353A","Neutral":"#D7C4BB", "Positive": "#86C166"}
    fig = px.pie(df, values='count', names='tag', color='tag',
                 title='Sentiment Distribution on Twitter\nKeyword: blockchain',
                color_discrete_map = palette)
    return fig
# Running the app in port 7000 localhost.
if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port=7000, debug=True)