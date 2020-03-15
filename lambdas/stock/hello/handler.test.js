const stockHello = require('./handler.js');
const status = require('http-status');

describe('Stock Hello Lambda', () => {
    beforeAll(() => {
        process.env.ORIGIN = '*'
    });

    describe('GET Requests', () => {
        const handler = stockHello({});

        test('returns correct response', async () => {
            const result = await handler({
                httpMethod: 'GET'
            });

            expect(result.statusCode).toEqual(status.OK);
            expect(JSON.parse(result.body)).toEqual({
                message: 'GET hello!'
            });
        });
    });

    describe('POST Requests', () => {
        const handler = stockHello({});

        test('returns correct response', async () => {
            const result = await handler({
                httpMethod: 'POST'
            });

            expect(result.statusCode).toEqual(status.OK);
            expect(JSON.parse(result.body)).toEqual({
                message: 'POST hello!'
            });
        });
    });
});
