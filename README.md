# google-drive-with-aws
CloudFormation templates, Lambda function, and scripts to demo how to pull files from S3 and push to Google Drive.

![Google Drive Lamba](https://user-images.githubusercontent.com/2858742/119348215-8f336f00-bc6a-11eb-9cf9-43cda85259a4.jpeg)

## Instructions

Please see my Medium article with step-by-step instructions with more detail.
https://dspenard.medium.com/push-aws-s3-files-to-google-drive-dabf5005a278

#### Requirements to set up the demo
- Python3 installed
- zip installed
- AWS CLI installed and running with permissions to use CloudFormation and S3 (I recommend just using AWS CloudShell with your user granted the necessary permissions)
- Google Service Account created, Google Drive API enabled for a Google Drive, and a shared folder created with write permission given to the service account

#### Steps

Please note that this is not fully automated and the scripts can be run one-by-one, but they require a few manual changes before doing so.  Each of the Bash files has details on what might need adjusting before running.

- git clone https://github.com/dspenard/google-drive-with-aws.git
- cd google-drive-with-aws/scripts
- bash build-bucket-and-ssm-resources.sh
- modify SSM parameters via console to enter your Google service account credentials json and the shared drive ID
- bash copy-test-files.sh
- bash build-packages.sh
- bash build-lambda-resources.sh
- go to the Lambda function and create a test using testdata/lambda-test.json to test the function
- clean up the resources

#### Issues

If you get the error 'Lambda was unable to decrypt the environment variables because KMS access was denied', just redeploy the Lambda function and it will go away.  I haven't had time to look into this further.
https://github.com/serverless/examples/issues/279
