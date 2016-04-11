/* FII - a Fundo de Investimento Imobiliário */
CREATE TABLE fii(
    code TEXT PRIMARY KEY,
    company TEXT,
    fund TEXT,
    type TEXT,
    url TEXT,
    error BOOLEAN
);

/* A user that watches the FII */
CREATE TABLE watcher(
    id SERIAL PRIMARY KEY,
    email TEXT UNIQUE,
    status TEXT
);

/* N-N mapping from Watcher to FII */
CREATE TABLE watcher_fii_map(
    watcher_id bigint REFERENCES watcher(id),
    fii_code TEXT REFERENCES fii(code),

    PRIMARY KEY (watcher_id, fii_code)
);

/* Scraped logs from a FII */
CREATE TABLE fii_log(
    id SERIAL PRIMARY KEY,
    fii_code TEXT REFERENCES fii(code),
    html TEXT,
    subject TEXT,
    link TEXT,
    notification_date TIMESTAMP
);
