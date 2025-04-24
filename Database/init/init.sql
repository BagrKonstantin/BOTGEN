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
    bot_id                 SERIAL PRIMARY KEY,
    user_id                INT                   NOT NULL,
    name               TEXT    DEFAULT 'Bot',
    is_launched            BOOLEAN DEFAULT FALSE NOT NULL,
    token                  TEXT           NOT NULL,
    data_json              JSON                  NOT NULL,
    greeting_message       TEXT,
    notify_on_sold         BOOLEAN DEFAULT FALSE NOT NULL,
    notify_on_out_of_stock BOOLEAN DEFAULT FALSE NOT NULL,
    notify_on_new_user  BOOLEAN DEFAULT FALSE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
);

CREATE TABLE bot_users
(
    bot_user_id SERIAL PRIMARY KEY,
    bot_id      INT    NOT NULL,
    tel_id      BIGINT NOT NULL,
    FOREIGN KEY (bot_id) REFERENCES bots (bot_id) ON DELETE CASCADE
);

CREATE TABLE product_types
(
    product_type_id SERIAL PRIMARY KEY,
    bot_id          INT  NOT NULL,
    name            TEXT NOT NULL,
    price           INT,
    FOREIGN KEY (bot_id) REFERENCES bots (bot_id) ON DELETE CASCADE
);

CREATE TABLE products
(
    product_id      SERIAL PRIMARY KEY,
    product_type_id INT     NOT NULL,
    file_id         TEXT    NOT NULL,
    is_sold         BOOLEAN NOT NULL DEFAULT FALSE,
    bot_user_id     INT,
    FOREIGN KEY (product_type_id) REFERENCES product_types (product_type_id) ON DELETE CASCADE,
    FOREIGN KEY (bot_user_id) REFERENCES bot_users (bot_user_id) ON DELETE CASCADE

);
