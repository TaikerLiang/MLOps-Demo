from typing import Tuple
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from io import StringIO
import json
import pickle
import base64

from airflow.decorators import task
from sklearn.ensemble import RandomForestClassifier
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from sklearn.metrics import make_scorer, accuracy_score, precision_score, recall_score, f1_score
from sklearn import model_selection


@task
def serialize_data(data):
    # Use pickle to serialize the data (DataFrame or Series)
    pickled_data = pickle.dumps(data)
    # Encode the pickled data with base64 to get a string representation
    base64_encoded_data = base64.b64encode(pickled_data).decode('utf-8')
    return base64_encoded_data

@task
def deserialize_data(base64_encoded_data):
    # Decode the base64 encoded string to get the pickled data
    pickled_data = base64.b64decode(base64_encoded_data.encode('utf-8'))
    # Use pickle to deserialize the data back to its original form (DataFrame or Series)
    data = pickle.loads(pickled_data)
    return data



@task(multiple_outputs=True)
def get_dataset(data: pd.DataFrame) -> dict:
    y = data["Survived"]
    features = ["Pclass", "Sex", "SibSp", "Parch", "AgeLevel"]
    X = pd.get_dummies(data[features])
    
    # # Serialize DataFrame and Series
    # serialized_X = serialize_dataframe(X)
    # serialized_y = serialize_dataframe(y.to_frame())  # Convert Series to DataFrame for serialization

    return {
        "X": X,
        "y": y
    }


@task
def train_model(X: pd.DataFrame, y: pd.Series) -> RandomForestClassifier:
    model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=1)
    model.fit(X, y)

    return model


@task
def evaluate_model(model, X, y) -> dict:
    scoring = {
        'accuracy': 'accuracy',
        'precision': 'precision',
        'recall': 'recall',
        'f1_score': 'f1'
    }

    kfold = model_selection.KFold(n_splits=10, shuffle=True, random_state=42)

    results = model_selection.cross_validate(estimator=model,
                             X=X,
                             y=y,
                             cv=kfold,
                             scoring=scoring,
                             return_train_score=False)

    for metric_name, scores in results.items():
        print(f"{metric_name}: {np.mean(scores):.3f} (+/- {np.std(scores):.3f})")

    return results
