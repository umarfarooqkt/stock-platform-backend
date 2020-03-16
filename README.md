# stock-platform-backend

This repository contains all the code for the serverless backend using a SAM template. It also defines the 
infrastructure in the CloudFormation stack to support the project (e.g. databases, networking, etc.).

## Initializing

### Local requirements

- Node.js & [Yarn](https://yarnpkg.com/en/docs/install)
- [SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
- [Docker](https://www.docker.com/products/docker-desktop)

```
$ yarn install
```

## Running API Locally

Ensure the docker engine is running and run:

```
$ yarn start
```

## Running tests

Run from the root of the project or lambda function directories:
`yarn test`
