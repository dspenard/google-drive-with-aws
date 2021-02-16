# google-drive-with-aws
CloudFormation templates, Lambda function, and scripts to demo how to pull files from S3 and push to Google Drive.

## Instructions

Sorry, I do plan to clean this up and provide details on everything with screenshots and explanations.

#### Requirements to set up the demo
- Python3 installed
- zip installed
- AWS CLI installed and running with permissions to use CloudFormation and S3 (I recommend just using AWS CloudShell with your user granted the necessary permissions)
- Google Service Account created, Google Drive API enabled for a Google Drive, and a shared folder created with write permission given to the service account

#### Steps
- clone this repo
- cd scripts
- bash build-bucket-and-ssm-resources.sh
- modify SSM parameters via console to enter your Google service account credentials json and the shared drive ID
- bash copy-test-files.sh
- bash build-packages.sh
- bash build-lambda-resources.sh
- go to the Lambda function and create a test using testdata/lambda-test.json to test the function
