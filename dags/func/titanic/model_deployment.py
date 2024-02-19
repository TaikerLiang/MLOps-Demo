import pickle
import tempfile

from airflow.decorators import task

@task
def save_model(model) -> str:
    # Serialize the model and save it to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pkl') as tmp:
        pickle.dump(model, tmp)
        tmp_path = tmp.name  # Get the path of the temporary file

    return tmp_path