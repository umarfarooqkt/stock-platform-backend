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
        // Remove root resource & directory lambda from results
        const apiId = event.requestContext.apiId;
        const resources = (await deps.getResources(apiId)).items
            .filter((item) => item.path !== '/' && item.path !== '/directory');

        // Extract top-level resources as services
        const services = resources
            .filter((item) => item.path === `/${item.pathPart}`)
            .map((item) => ({ name: item.pathPart }));

        // Add resources to each service
        for (const service of services) {
            service.resources = resources
                .filter((item) => item.path.startsWith(`/${service.name}/`) && item.resourceMethods != null)
                .map((item) => ({
                    endpoint: item.path,
                    methods: Object.keys(item.resourceMethods)
                }));
        }

        return response(status.OK, { services });
    } catch (err) {
        console.error(err);
        return response(status.INTERNAL_SERVER_ERROR, {
            error: err.message
        });
    }
};
