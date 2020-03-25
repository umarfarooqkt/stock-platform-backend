const apiDirectory = require('./handler.js');
const status = require('http-status');

describe('API Directory Lambda', () => {
    let handler;
    const getResourcesFn = jest.fn();

    beforeEach(() => {
        handler = apiDirectory({
            getResources: getResourcesFn
        })
    });

    afterEach(() => {
        getResourcesFn.mockReset();
    });

    test('correctly formats API Gateway resources', async () => {
        getResourcesFn.mockResolvedValueOnce({
            items: [{
                "id": "1",
                "path": "/"
            }, {
                "id": "2",
                "parentId": "1",
                "pathPart": "test",
                "path": "/test"
            }, {
                "id": "3",
                "parentId": "2",
                "pathPart": "hello",
                "path": "/test/hello",
                "resourceMethods": {
                    "GET": {},
                    "POST": {},
                    "OPTIONS": {}
                }
            }, {
                "id": "4",
                "parentId": "1",
                "pathPart": "directory",
                "path": "/directory",
                "resourceMethods": {
                    "GET": {}
                }
            }]
        });
        const result = await handler({
            requestContext: {
                apiId: 'test123'
            }
        });

        expect(getResourcesFn).toHaveBeenCalledWith('test123');
        expect(result.statusCode).toEqual(status.OK);
        expect(result.body).toEqual(JSON.stringify({
            services: [{
                name: "test",
                resources: [{
                    endpoint: "/test/hello",
                    methods: [ "GET", "POST", "OPTIONS" ]
                }]
            }]
        }));
    });
});
