const analysisHello = require('./handler.js');
const status = require('http-status');

describe('Analysis Hello Lambda', () => {
    beforeAll(() => {
        process.env.ORIGIN = '*'
    });

    describe('GET Requests', () => {
        const handler = analysisHello({});

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
        const handler = analysisHello({});

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
