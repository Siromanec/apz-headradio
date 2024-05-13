db.createUser({
    user: "root",
    pwd: "root_pass",
    roles: [
        {
            role: "readWrite",
            db: "profile_db"
        },
    ],
});

db.createCollection("profile",
    {
        validator: {
            $jsonSchema: {
                bsonType: "object",
                required: ["username", "profile_picture", "selected_music", "motto"],
                properties: {
                    username: {
                        bsonType: "string",
                        description: "must be a string and is required",
                    },
                    profile_picture: {
                        bsonType: "string",
                        description: "must be a string and is required",
                    },
                    selected_music: {
                        bsonType: "string",
                        description: "must be a string and is required",
                    },
                    motto: {
                        bsonType: "string",
                        description: "must be a string and is required",
                    },
                },
            },
        },
    });

