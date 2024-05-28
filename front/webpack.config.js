module.exports = {
    resolve: {
        fallback: {
            http: require.resolve('stream-http'),
            https: require.resolve('https-browserify'),
            querystring: require.resolve('querystring-es3'),
        },
    },
};