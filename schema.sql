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
    address TEXT,
    coord_x FLOAT,
    coord_y FLOAT,
    is_24h BOOLEAN,
    open_mon TIME,
    close_mon TIME,
    open_tue TIME,
    close_tue TIME,
    open_wed TIME,
    close_wed TIME,
    open_thu TIME,
    close_thu TIME,
    open_fri TIME,
    close_fri TIME,
    open_sat TIME,
    close_sat TIME,
    open_sun TIME,
    close_sun TIME
);

CREATE TABLE restaurants_ratings(
    id SERIAL PRIMARY KEY,
    comment TEXT,
    rating INTEGER,
    user_id INTEGER REFERENCES users,
    restaurant_id INTEGER REFERENCES restaurants,
    sent_at TIMESTAMP
);

CREATE TABLE categories(
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE
);

CREATE TABLE restaurants_categories(
    id SERIAL PRIMARY KEY,
    restaurant_id INTEGER REFERENCES restaurants,
    category_id INTEGER REFERENCES categories
);

CREATE TABLE types(
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE
);

CREATE TABLE restaurants_types(
    id SERIAL PRIMARY KEY,
    restaurant_id INTEGER REFERENCES restaurants,
    type_id INTEGER REFERENCES types
);

-- Add default admin

INSERT INTO users (username, password, role) VALUES ('admin', 'admin', 'admin');

-- Add default categories and types for initial launch

INSERT INTO categories (name) VALUES ('Hampurilaiset'), ('Salaatti'), ('Jälkiruoka'), ('Kasvisruoka'), ('Amerikkalainen'), ('Pizza'), ('Vegaani'), ('Jäätelö'),
('Katuruoka'), ('Voileivät'), ('Kebab'), ('Japanilainen'), ('Nuudelit'), ('Aamupala'), ('Terveellinen'), ('Keitto'), ('Sushi'), ('Välimerellinen'), ('Italialainen'),
('Meksikolainen'), ('Kulhoruuat'), ('Nepalilainen'), ('Wings');

INSERT INTO types (name) VALUES ('Hieno ruokailu'), ('Rento ruokailu'), ('Perhetyyli'), ('Buffet'), ('Kahvila'), ('Pikaruoka'), ('Ruoka-auto/koju');

-- Add default restaurants for initial launch

INSERT INTO restaurants (name, description, address, coord_x, coord_y, is_24h)
VALUES ('McDonald''s Helsinki Kamppi', 'Pitkäikäinen pikaruokaketju, joka tunnetaan hampurilaisista ja ranskalaisista.',
'Fredrikinkatu 46, 00100 Helsinki', 60.16902613320498, 24.930135096411046, TRUE);

INSERT INTO restaurants (name, description, address, coord_x, coord_y, is_24h, open_mon, close_mon, open_tue, close_tue, open_wed, close_wed, open_thu, close_thu, open_fri, close_fri, open_sat, close_sat, open_sun, close_sun) 
VALUES ('Espresso House Kamppi HKI', 'Espresso House on Pohjoismaiden suurin kahvilaketju noin 500 kahvilalla Suomessa, Ruotsissa, Norjassa, Tanskassa ja Saksassa.',
'Urho Kekkosen katu 1, 00100 Helsinki', 60.16879541517622, 24.93252736590296, FALSE,
'06:30:00', '22:00:00', '06:30:00', '22:00:00', '06:30:00', '22:00:00', '06:30:00', '22:00:00', '06:30:00', '22:00:00', '07:00:00', '22:00:00', '08:30:00', '21:00:00');

INSERT INTO restaurants (name, description, address, coord_x, coord_y, is_24h, open_mon, close_mon, open_tue, close_tue, open_wed, close_wed, open_thu, close_thu, open_fri, close_fri, open_sat, close_sat, open_sun, close_sun) 
VALUES ('Taco Bell Tennispalatsi', 'Meksikolaista pikaruokaa tarjoileva ketjuravintola, josta saa esimerkiksi tacoja, quesadilloja ja nachoja.',
'Fredrikinkatu 65, 00100 Helsinki', 60.16912103101747, 24.930496051661258, FALSE,
'10:30:00', '00:00:00', '10:30:00', '00:00:00', '10:30:00', '00:00:00', '10:30:00', '00:00:00', '10:30:00', '17:00:00', '10:30:00', '17:00:00', '11:00:00', '23:00:00');

INSERT INTO restaurants (name, description, address, coord_x, coord_y, is_24h, open_mon, close_mon, open_tue, close_tue, open_wed, close_wed, open_thu, close_thu, open_fri, close_fri, open_sat, close_sat) 
VALUES ('Ravintola Factory Kamppi', 'Suositut buffet-lounaat ja salaattibaarit pääkaupunkiseudulla. Meiltä myös catering- ja juhlapalvelut!',
'Runeberginkatu 3, 00100 Helsinki', 60.16884251321125, 24.928836392310558, FALSE,
'10:30:00', '15:00:00', '10:30:00', '15:00:00', '10:30:00', '20:00:00', '10:30:00', '20:00:00', '10:30:00', '20:00:00', '12:00:00', '20:00:00');

