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
                required: ["username"],
                properties: {
                    username: {
                        bsonType: "string",
                        description: "must be a string and is required and is unique",
                    },
                    profile_picture: {
                        bsonType: "string",
                        description: "must be a string and is optional",
                    },
                    selected_music: {
                        bsonType: "string",
                        description: "must be a string and is optional",
                    },
                    motto: {
                        bsonType: "string",
                        description: "must be a string and is optional",
                    },
                },
            },
        },
    });

db.profile.createIndex({ username: 1 }, { unique: true });

