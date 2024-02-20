# MLOps-Demo

MLOps-Demo is a project aimed at demonstrating how to build a machine learning (ML) pipeline using Python and Airflow. In this project, we will illustrate how to use Airflow to automatically export the trained model to AWS S3.

We have chosen the [Titanic competition](https://www.kaggle.com/competitions/titanic), a well-known challenge on Kaggle, as our example dataset.

# Installation

Please make sure you have installed the following services in your local environment for developing.

### Docker & Docker-compose


We will use docker-compose to start the airflow service.

* https://docs.docker.com/desktop/
* https://docs.docker.com/compose/install/


### LocalStack

We will use the LocalStack to mock AWS S3 service

* https://www.localstack.cloud/


# Environment Setting

> .env

* For the AIRFLOW_UID you can use this command to get it `echo $(id -u)`
* For the AIRFLOW_PROJ_DIR you should input your local folder path

```
AIRFLOW_UID=
AIRFLOW_PROJ_DIR= 
_AIRFLOW_WWW_USER_USERNAME=airflow
_AIRFLOW_WWW_USER_PASSWORD=airflow
_PIP_ADDITIONAL_REQUIREMENTS=pandas numpy boto3 scikit-learn
```


### LocalStack Setting

After install the LocalStack, we need to create the fake AWS config/credentials in our local environment. 

> ~/.aws/config

```
[profile localstack]
region=us-east-1
output=json

```

> ~/.aws/credentials

```
[localstack]
aws_access_key_id = test
aws_secret_access_key = test
```


### Airflow Connections

After completing the LocalStack setting, we need to add a new connection setting through the Airflow Web UI. please go to the Admin->Connections to create a new one.

```
Connection Id: aws_localstack
Connection Type: Amazon Web Services
AWS Access Key ID: test
AWS Secret Access Key: test
Extra: {
  "region_name": "us-east-1",
  "endpoint_url": "http://host.docker.internal:4566"
}
```


# ML Pipeline Lifecycle

![image](https://github.com/TaikerLiang/MLOps-Demo/assets/850956/f590af78-91d4-4ef1-a171-0e71c48f0c22)


# Folder Structure
* dags: This directory contains the main DAG (Directed Acyclic Graph) functions.
* dags/func: Within this directory, sub-folders are organized for modularization. Each folder name corresponds to a main DAG function. Inside each sub-folder, the entire ML pipeline is divided into different steps, with each step having its own file to complete the related function.


# Final Airflow Graph

![image](https://github.com/TaikerLiang/MLOps-Demo/assets/850956/6b080c9a-e1bb-407e-ac62-545fcd23782f)



# Reference

* https://www.kaggle.com/competitions/titanic
* https://www.kaggle.com/code/alexisbcook/titanic-tutorial
* https://docs.localstack.cloud/overview/
* https://proclusacademy.com/blog/practical/k-fold-cross-validation-sklearn/
