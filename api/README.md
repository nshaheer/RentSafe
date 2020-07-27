## API

There are 2 main goals of the Public API:

### Submit for analysis
Submit paragraphs for analysis. This involves compiling txt files for AWS Comprehend, uploading them to S3, starting AWS Comprehend jobs and storing metadata in MongoDB.

### Get analysis
Get the analysis for a given lease.

If the lease analysis is complete then we need to simply get the results of the analysis in MongoDB and return them.

If not, engage the `services` to fetch Entity Recognition and Classification job results, analyse them and update the lease in MongoDB

The above 2 goals are hence encapsulated in the `use_cases` folder. These usecases, which is the interface exposed to the public via HTTP utilize `infrastructure` and `services` as needed.

## Infrastructure
3rd aprty components critical to RentSafe.

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
`cd api && FLASK_APP=rest.py && FLASK_ENV=development && python3 -m flask run`