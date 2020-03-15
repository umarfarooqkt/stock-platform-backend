const {
    AWS_REGION
} = process.env;

const aws = require('aws-sdk');
aws.config.update({ region: AWS_REGION });

// Use dependency injection to allow for easier unit testing
module.exports.handler = require('./handler.js')({

});

