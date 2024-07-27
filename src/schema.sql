CREATE TABLE links (
    id integer PRIMARY KEY NOT NULL,
    original_url text NOT NULL,
    new_url text NOT NULL,
    password text NOT NULL,
    retries int,
    attempts int
);
