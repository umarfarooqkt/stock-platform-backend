module.exports = (deps) => async (event) => {
    try {
        const userSub = event.request.userAttributes.sub;

        if (event.triggerSource === 'PostConfirmation_ConfirmSignUp') {
            await deps.publishUserCreateMessage({
                sub: userSub
            });

            console.log(`Published message to User-Create SNS for user sub: ${userSub}`);
        }

        return event;
    } catch (err) {
        console.error(err);
    }
};
