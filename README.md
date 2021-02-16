# google-drive-with-aws
CloudFormation templates, Lambda function, and scripts to demo how to pull files from S3 and push to Google Drive.

## Instructions

Sorry, I do plan to clean this up and provide details on creating the Google Service account and using the Google Shared Drive API.

- cd scripts
- bash build-bucket-and-ssm-resources.sh
- modify SSM parameters via console to enter your Google service account credentials json and the shared drive ID
- bash copy-test-files.sh
- bash build-packages.sh
- bash build-lambda-resources.sh
- go to the Lambda function and create a test using testdata/lambda-test.json to test the function
