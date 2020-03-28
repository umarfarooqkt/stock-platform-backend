#!/bin/bash
STACK_NAME=stock-platform-backend
BUILD_BUCKET=cs4471-group1-project-backend-builds
FRONTEND_BUCKET=cs4471-group1-project-frontend
FRONTEND_DOMAIN=cs4471-stock-platform.xyz
FRONTEND_LOGIN_SUBDOMAIN=cs4471-group1-project-login

sam build
sam deploy --stack-name $STACK_NAME --capabilities CAPABILITY_IAM --confirm-changeset --s3-bucket $BUILD_BUCKET \
  --parameter-overrides ParameterKey=FrontendBucketName,ParameterValue=$FRONTEND_BUCKET \
  ParameterKey=FrontendDomain,ParameterValue=$FRONTEND_DOMAIN \
  ParameterKey=FrontendLoginSubDomain,ParameterValue=$FRONTEND_LOGIN_SUBDOMAIN
