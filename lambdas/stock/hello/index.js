const {
    AWS_REGION
} = process.env;

const aws = require('aws-sdk');
aws.config.update({ region: AWS_REGION });

// TODO: Connect to MySQL

// Use dependency injection to allow for easier unit testing
module.exports.handler = require('./handler.js')({
    // TODO: Add DAO functions here
});

