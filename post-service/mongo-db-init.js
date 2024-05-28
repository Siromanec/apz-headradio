db.createUser({
    user: "root",
    pwd: "root_pass",
    roles: [
        {
            role: "readWrite",
            db: "post_db"
        },
    ],
});

db.createCollection("posts",
    {
        validator: {
            $jsonSchema: {
                bsonType: "object",
                required: ["username", "time", "article"],
                properties: {
                    username: {
                        bsonType: "string",
                        description: "must be a string and is required",
                    },
                    time: {
                        bsonType: "date",
                        description: "must be a date and is required",
                    },
                    article: {
                        bsonType: "string",
                        description: "must be a string and is required",
                    },
                },
            },
        },
    });

