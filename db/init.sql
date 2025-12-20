CREATE TABLE IF NOT EXISTS word_stats (
   id SERIAL PRIMARY KEY,
   total_words INTEGER NOT NULL
);
INSERT INTO word_stats (total_words)
SELECT 0
WHERE NOT EXISTS (SELECT 1 FROM word_stats);
