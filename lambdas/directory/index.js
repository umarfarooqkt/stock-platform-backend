const {
    AWS_REGION
} = process.env;

const aws = require('aws-sdk');
aws.config.update({ region: AWS_REGION });

const apiGateway = new aws.APIGateway({ apiVersion: '2015-07-09' });

// Use dependency injection to allow for easier unit testing
module.exports.handler = require('./handler.js')({
    getResources: (apiId) => apiGateway.getResources({
        restApiId: apiId,
        limit: 500
    }).promise()
});

