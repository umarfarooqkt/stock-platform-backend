const userRegistrationHello = require('./handler.js');

describe('User Registration Hello Lambda', () => {
    const handler = userRegistrationHello({});

    test('runs successfully', async () => {
        const result = await handler({});

        expect(result).toEqual({});
    });
});
