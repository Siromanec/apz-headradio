with open("./node_modules/react-scripts/config/webpack.config.js", "r") as f:
    contents = f.readlines()


fix = """    resolve: {
        fallback: { 
            http: require.resolve('stream-http'),
            https: require.resolve('https-browserify'),
            querystring: require.resolve('querystring-es3'),
        },
    },\n"""

contents.insert(len(contents)-2, fix)

with open("./node_modules/react-scripts/config/webpack.config.js", "w") as f:
    contents = "".join(contents)
    f.write(contents)
print(contents)
print("Config fixed")