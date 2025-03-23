CREATE TABLE users
(
    user_id  SERIAL PRIMARY KEY,
    tel_id   BIGINT UNIQUE NOT NULL,
    username TEXT
);

CREATE TABLE subscriptions
(
    subscription_id SERIAL PRIMARY KEY,
    user_id         INT       NOT NULL,
    start_date      TIMESTAMP NOT NULL,
    expiration_date TIMESTAMP NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
);

CREATE TABLE bots
(
    bot_id    SERIAL PRIMARY KEY,
    user_id   INT         NOT NULL,
    token     TEXT UNIQUE NOT NULL,
    data_json JSONB       NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
);

CREATE TABLE bot_users
(
    bot_user_id SERIAL PRIMARY KEY,
    bot_id      INT    NOT NULL,
    tel_id      BIGINT NOT NULL,
    FOREIGN KEY (bot_id) REFERENCES bots (bot_id) ON DELETE CASCADE
);

CREATE TABLE products
(
    product_id  SERIAL PRIMARY KEY,
    bot_id      INT            NOT NULL,
    name        TEXT           NOT NULL,
    description TEXT,
    image_url   TEXT,
    price       NUMERIC(10, 2) NOT NULL,
    FOREIGN KEY (bot_id) REFERENCES bots (bot_id) ON DELETE CASCADE
);

CREATE TABLE purchases
(
    purchase_id SERIAL PRIMARY KEY,
    product_id  INT NOT NULL,
    user_bot_id INT NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products (product_id) ON DELETE CASCADE,
    FOREIGN KEY (user_bot_id) REFERENCES bot_users (bot_user_id) ON DELETE CASCADE
);