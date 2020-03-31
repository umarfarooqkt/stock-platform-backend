const {
    AWS_REGION,
    USER_CREATE_SNS_TOPIC
} = process.env;

const aws = require('aws-sdk');
aws.config.update({ region: AWS_REGION });

const sns = new aws.SNS({ apiVersion: '2010-03-31' });

// Use dependency injection to allow for easier unit testing
module.exports.handler = require('./handler.js')({
    publishUserCreateMessage: (message) => sns.publish({
        TopicArn: USER_CREATE_SNS_TOPIC,
        Message: JSON.stringify(message)
    }).promise()
});

