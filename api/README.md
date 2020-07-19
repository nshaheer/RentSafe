## API

There are 3 main goals of the API:

### Submit for analysis
Submit paragraphs for analysis. This involves compiling CSVs for AWS Comprehend, uploading them to S3 and starting AWS Comprehend jobs.

### Get analysis
Get the analysis for a given lease. This is a simple call to get the lease from our lease storage.

### Update analysis
When an ML job is completed, update the results. This happens when AWS Comprehend uploads the results of a job to S3, triggering an SNS notification. We need to interpret the results of the job and update the lease.

The above 3 goals are hence encapsulated in the `use_cases` folder. The API Server (Flask|Falcon|FastAPI) calls these usecases.