CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT
);

CREATE TABLE restaurants(
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    description TEXT,
    opening_time TIME,
    closing_time TIME
);

CREATE TABLE restaurants_ratings(
    id SERIAL PRIMARY KEY,
    comment TEXT,
    rating INTEGER,
    user_id INTEGER REFERENCES users,
    restaurant_id INTEGER REFERENCES restaurants,
    sent_at TIMESTAMP
);

CREATE TABLE groups(
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE
)

CREATE TABLE restaurants_groups(
    id SERIAL PRIMARY KEY,
    restaurant_id INTEGER REFERENCES restaurants,
    group_id INTEGER REFERENCES groups
)

INSERT INTO restaurants (name, description, opening_time, closing_time)
VALUES ('McDonald''s Helsinki Kamppi', 'Pitkäikäinen pikaruokaketju, joka tunnetaan hampurilaisista ja ranskalaisista.', '00:00:00', '23:59:00');

INSERT INTO restaurants (name, description, opening_time, closing_time)
VALUES ('Espresso House Kamppi HKI', 'Espresso House on Pohjoismaiden suurin kahvilaketju noin 500 kahvilalla Suomessa, Ruotsissa, Norjassa, Tanskassa ja Saksassa.', '06:30:00', '22:00:00');

INSERT INTO restaurants (name, description, opening_time, closing_time)
VALUES ('Taco Bell Kamppi', 'Meksikolaista pikaruokaa tarjoileva ketjuravintola, josta saa esimerkiksi tacoja, quesadilloja ja nachoja.', '10:30:00', '00:00:00');

INSERT INTO restaurants (name, description, opening_time, closing_time)
VALUES ('Ravintola Factory Kamppi', 'Suositut buffet-lounaat ja salaattibaarit pääkaupunkiseudulla. Meiltä myös catering- ja juhlapalvelut!', '10:30:00', '20:00:00');