-- Portable reference schema; the Python loader creates the same SQLite table.
CREATE TABLE IF NOT EXISTS economic_indicators (
    dataset TEXT NOT NULL,
    date DATE NOT NULL,
    value REAL NOT NULL,
    unit TEXT NOT NULL,
    PRIMARY KEY (dataset, date)
);

