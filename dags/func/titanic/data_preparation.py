import os
import tempfile
from io import StringIO

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

from airflow.decorators import task
from airflow.providers.amazon.aws.hooks.s3 import S3Hook


# Define a function that categorizes the age
def categorize_age(age):
    if pd.isnull(age):
        return 'unknown'
    elif age < 30:
        return 'young'
    elif 30 <= age <= 60:
        return 'medium'
    else:
        return 'old'

@task
def delete_temp_file(temp_file_name):
    if os.path.isfile(temp_file_name):
        os.remove(temp_file_name)


@task
def load_data_from_s3() -> pd.DataFrame:
    s3_hook = S3Hook(aws_conn_id='aws_localstack')
    bucket_name = 'airflow'
    object_key = 'titanic/raw.csv'


    # Get the content of the file
    csv_content = s3_hook.read_key(key=object_key, bucket_name=bucket_name)
    csv_file_like_object = StringIO(csv_content)
    data = pd.read_csv(csv_file_like_object)

    print("raw data", data.head())

    return data


@task
def data_preprocessing(data: pd.DataFrame) -> pd.DataFrame:
    # Apply the function to the 'Age' column to create a new 'AgeLevel' column
    data['AgeLevel'] = data['Age'].apply(categorize_age)

    # Display the DataFrame to verify the new column
    print(data[['Age', 'AgeLevel']].head())

    return data


@task
def export_the_training_data_to_s3(data: pd.DataFrame) -> str:
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp:
        temp_file_name = tmp.name
        # Export DataFrame to the temporary CSV file
        data.to_csv(temp_file_name, index=False)

    return temp_file_name



