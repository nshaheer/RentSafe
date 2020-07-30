## API

There are 2 main goals of the Public API:

### Submit for analysis
Submit paragraphs for analysis. This involves compiling txt files for AWS Comprehend, uploading them to S3, starting AWS Comprehend jobs and storing metadata in MongoDB.

### Get analysis
Get the analysis for a given lease.

If the lease analysis is complete then we need to simply get the results of the analysis in MongoDB and return them.

If not, engage `services` to fetch Entity Recognition and Classification job results, analyze them and update the lease in MongoDB.

The above 2 goals are hence encapsulated in the `use_cases` folder. These usecases, providing the interface exposed to the public via HTTP, utilize `infrastructure` and `services` as needed.

## Infrastructure
3rd party components critical to RentSafe.

### Entity Recognizer
A minimal interface wrapping the AWS `boto3` library and it's AWS Comprehend interface for entity recognition.

### Classifier
A minimal interface wrapping the AWS `boto3` library and it's AWS Comprehend interface for custom classification.

### Storage
A minimal interface wrapping the MongoDB Python client for adding and updating leases.

## Services

### Analyze Entity Recognition Results
Process Entity Recognition results in the context of a lease.

### Analyze Classification Results
Process Classification results in the context of a lease.

## Local Development
`cd api && export FLASK_APP=app.py && export FLASK_ENV=development && python3 -m flask run`

To run a faster API that returns mock data for local testing, `cd api && export FLASK_APP=dummy_rest.py && export FLASK_ENV=development && python3 -m flask run`

A Postman export is available in `docs/` to visualize the exact requests and responses.

## Background Tasks
`celery worker -A app.celery --beat -l INFO`

## Server Access
`ssh -i .aws/RentSafe.pem ubuntu@ec2-15-223-126-32.ca-central-1.compute.amazonaws.com`

### Redis Setup
Install using:

https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-redis-on-ubuntu-18-04

Update `/etc/hosts` by adding `127.0.0.1 redis` to it.

### Gunicorn and Nginx Setup
https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04