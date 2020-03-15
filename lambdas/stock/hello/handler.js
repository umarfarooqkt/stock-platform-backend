const status = require('http-status');

const response = (statusCode, body) => ({
    statusCode,
    body: JSON.stringify(body),
    headers: {
        'Access-Control-Allow-Origin': process.env.ORIGIN
    }
});

module.exports = (deps) => async (event) => {
    try {
        switch (event.httpMethod) {
            case 'GET':
                return response(status.OK, { message: 'GET hello!' });

            case 'POST':
                return response(status.OK, { message: 'POST hello!' });

            default:
                return response(status.METHOD_NOT_ALLOWED);
        }
    } catch (err) {
        console.error(err);
        return response(status.INTERNAL_SERVER_ERROR, {
            error: err.message
        });
    }
};
