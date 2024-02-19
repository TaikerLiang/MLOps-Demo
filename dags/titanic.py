from datetime import datetime, timedelta
import json
import pickle
import base64

import pandas as pd
from airflow.decorators import task
from airflow.decorators import dag
from airflow.utils.dates import days_ago
from airflow.providers.amazon.aws.transfers.local_to_s3 import LocalFilesystemToS3Operator
from airflow.utils.task_group import TaskGroup

from func.titanic.data_preparation import load_data_from_s3, data_preprocessing, export_the_training_data_to_s3, delete_temp_file
from func.titanic.model_training import get_dataset, train_model, evaluate_model
from func.titanic.model_deployment import save_model


@dag(schedule_interval='@daily', start_date=days_ago(1), catchup=False, tags=['example'])
def titanic_flow():


    with TaskGroup("data_preparation_group") as data_preparation:
        data = load_data_from_s3()
        train_data = data_preprocessing(data) # type: ignore
        tmp_filename = export_the_training_data_to_s3(train_data) # type: ignore

        upload_to_s3_task = LocalFilesystemToS3Operator(
            task_id='upload_to_s3',
            filename=tmp_filename, 
            dest_key='titanic/train.csv',
            dest_bucket='airflow',
            aws_conn_id='aws_localstack',  # Airflow AWS connection ID which can be created through the UI
            replace=True,
        )

        tmp_filename >> upload_to_s3_task
        upload_to_s3_task >> delete_temp_file(tmp_filename)


    with TaskGroup("model_training") as model_training:
        dataset = get_dataset(data=train_data)
        model = train_model(dataset['X'], dataset['y'])
        results = evaluate_model(model, dataset['X'], dataset['y'])


    with TaskGroup("model_deployment") as model_deployment:
        # Save the trained model to a temporary file
        model_file_path = save_model(model)

        # Task to upload the model to S3
        upload_model_to_s3 = LocalFilesystemToS3Operator(
            task_id='upload_model_to_s3',
            filename=model_file_path,
            dest_key='titanic/titanic_model.pkl',
            dest_bucket='airflow',
            aws_conn_id='aws_localstack', 
            replace=True,
        )

        results >> model_file_path >> upload_model_to_s3


dag = titanic_flow()
