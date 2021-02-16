#!/bin/bash

# before running this script modify ParentStackName to the stack just created with build-bucket-and-ssm-resources.sh

aws cloudformation create-stack \
    --stack-name google-drive-lambda \
    --template-body file://lambda-resources.yaml \
    --capabilities CAPABILITY_AUTO_EXPAND CAPABILITY_NAMED_IAM \
    --parameters ParameterKey=AWSAccount,ParameterValue=649389088215 \
        ParameterKey=ParentStackName,ParameterValue=google-drive-bucket-and-ssm