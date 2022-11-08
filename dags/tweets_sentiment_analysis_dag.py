'''
The dag script for airflow.
'''
import os

from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta

# folder settings
DAG_FOLDER = os.path.abspath(os.getcwd())
SCRIPTS_FOLDER = os.path.join(DAG_FOLDER, "..", "etl")

args = {
    'owner': 'William Chen',
    'depends_on_past': False,
    'start_date': datetime(2022, 11, 1),
}


# Setting the schedule and basic setting.
dag = DAG(
    dag_id='tweets_sentiment_app',
    default_args=args,
    schedule_interval='@hourly'
    params={
        'scripts_folder': SCRIPTS_FOLDER,
    }
)

'''
There are 3 BashOperator to 3 bash for each task.
'''
# Running tweet_sender.py
tweets_get = BashOperator(
    task_id='tweets_API_get',
    bash_command="""
        python3 {{params.scripts_folder}}/tweet_sender.py
    """,
    # trigger_rule = 'none_skipped',
    dag=dag,
)

# Running tweets_connect.py
tweets_processor = BashOperator(
    task_id='tweets_processing_and_save_to_Mongo',
    bash_command="""
        python3 {{params.scripts_folder}}/tweets_connect.py
    """,
    # trigger_rule = 'none_skipped',
    dag=dag,
)

# Running app.py
dash_app = BashOperator(
    task_id='running_live_update',
    bash_command="""
        python3 {{params.scripts_folder}}/app.py
    """,
    # trigger_rule = 'none_skipped',   
    dag=dag,
)

# Setting the skip task for the last.
skip = DummyOperator(
    task_id='skip',
    dag=dag
)

# Design the pipeline
tweets_get >> skip
tweets_processor >> skip
dash_app >> skip


if __name__ == "__main__":
    dag.cli()