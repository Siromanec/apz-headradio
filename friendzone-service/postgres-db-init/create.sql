
CREATE TABLE friends (
    USERNAME_FOLLOWS TEXT NOT NULL,
    USERNAME TEXT NOT NULL,
    PRIMARY KEY (USERNAME_FOLLOWS, USERNAME)
);