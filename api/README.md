## API

There are 4 main goals of the Public API:

### Submit for analysis
Submit document for analysis. This basically queues a document for text and thumbnail extraction which further queues it up for classification
and entity recognition.

### Get analysis
Get the analysis for a given lease.

### Email analysis
Email the analysis of a given lease to a recipient.

### Collect Questionnaire Responses
Collect Questionnaire responses by users.


Hence the primary entrypoint to the application is via `use_cases` which are either exposed to the public via the REST API or executed via `tasks`. The above 4 goals are hence encapsulated in the `use_cases` folder. All usecases utilize `infrastructure` and `services` as needed.

## Use Cases
1. EmailLeaseAnalysis
2. GetAnalysisResults
3. GetLeaseThumbnail
4. ProcessPendingAnalysis
5. SubmitLeaseForAnalysis
6. SubmitTextForAnalysis

## Infrastructure
1. Storage
2. Classifier
3. EntityRecogizer
4. Extractor

## Services
1. EmailService
2. ThumbnailService
3. AnalysisService
4. FormatterService
5. ImageConversionService

## Local Development
`docker-compose up`
`docker exec -it api bash`

## Background Tasks
`celery worker -A app.celery --beat -l INFO`


### Redis Setup
Install using:

https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-redis-on-ubuntu-18-04

Update `/etc/hosts` by adding `127.0.0.1 redis` to it.

### Gunicorn and Nginx Setup
https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04

