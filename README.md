# MLOps-Demo

MLOps-Demo is a project aimed at demonstrating how to build a machine learning (ML) pipeline using Python and Airflow.

We have chosen the [Titanic competition](https://www.kaggle.com/competitions/titanic), a well-known challenge on Kaggle, as our example dataset.

In this project, we will illustrate how to use Airflow to automatically export the trained model to AWS S3.


# Environment

### Docker & Docker-compose


We will use docker-compose to start the airflow service.

* https://docs.docker.com/desktop/
* https://docs.docker.com/compose/install/


### LocalStack

We will use the LocalStack to mock AWS S3 service

* https://www.localstack.cloud/


# Airflow Setting


# Reference

* https://www.kaggle.com/competitions/titanic
* https://www.kaggle.com/code/alexisbcook/titanic-tutorial
* https://docs.localstack.cloud/overview/
* https://proclusacademy.com/blog/practical/k-fold-cross-validation-sklearn/