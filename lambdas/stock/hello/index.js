const {
    AWS_REGION,
    RDS_SECRET_ARN,
    DB_OVERRIDE
} = process.env;

const aws = require('aws-sdk');
aws.config.update({ region: AWS_REGION });
const secretsManager = new aws.SecretsManager({ apiVersion: '2017-10-17' });

const mysql = require('mysql');
let connection;

const status = require('http-status');

module.exports.handler = async (...args) => {
    if (connection == null || connection.state === 'disconnected') {
        if (DB_OVERRIDE) {
            // TODO: Fix
            connection = mysql.createConnection({
                host: DB_OVERRIDE,
                user: 'root',
                password: 'abcd1234',
                database: 'stock'
            });
            console.log('DB_OVERRIDE set, connecting to local database..');
        } else {
            const secret = await secretsManager.getSecretValue({
                SecretId: RDS_SECRET_ARN
            }).promise();

            const {
                username: user,
                password,
                dbname: database,
                host
            } = JSON.parse(secret.SecretString);

            connection = mysql.createConnection({
                host,
                user,
                password,
                database
            });
        }

        try {
            await new Promise((resolve, reject) => {
                connection.connect((err) => {
                    if (err) {
                        reject(err);
                        return;
                    }
                    console.log('Connected to database');
                    resolve();
                })
            });
        } catch (err) {
            console.error(err);
            return {
                statusCode: status.INTERNAL_SERVER_ERROR,
                body: JSON.stringify({ error: 'Failed to connect to database' })
            }
        }
    } else {
        console.log('Using existing database connection');
    }

    // Use dependency injection to allow for easier unit testing
    return require('./handler.js')({
        // TODO: Add DAO functions here "getSomething: () => connect.query("SELECT ..."):"
    })(...args);
};

