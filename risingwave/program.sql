CREATE SOURCE IF NOT EXISTS transactions (
    id INT,
    from_account INT,
    to_account INT,
    amount INT,
    ts TIMESTAMP--,
    --WATERMARK FOR ts as ts - INTERVAL '5' SECOND
) WITH (
   connector='kafka',
   topic='input',
   properties.bootstrap.server='127.0.0.1:9092',
   scan.startup.mode='earliest'
) FORMAT PLAIN ENCODE JSON;

CREATE MATERIALIZED VIEW IF NOT EXISTS credits AS
SELECT
    to_account AS account, 
    sum(amount) AS credits
FROM
    transactions
GROUP BY
    to_account;

CREATE MATERIALIZED VIEW IF NOT EXISTS debits AS
SELECT
    from_account AS account, 
    sum(amount) AS debits
FROM
    transactions
GROUP BY
    from_account;

CREATE MATERIALIZED VIEW IF NOT EXISTS balance AS
SELECT
    credits.account AS account, 
    credits - debits AS balance
FROM
    credits,
    debits
WHERE
    credits.account = debits.account;

CREATE MATERIALIZED VIEW IF NOT EXISTS outer_join AS
SELECT
    t1.id AS id, 
    t2.id AS other_id
FROM
    (SELECT id FROM transactions) AS t1
LEFT JOIN
    (SELECT id FROM transactions) AS t2
ON
    t1.id = t2.id;

CREATE MATERIALIZED VIEW IF NOT EXISTS total AS
SELECT
    sum(balance) as sum_balance
FROM
    balance;
    
    
CREATE SINK sink1 FROM total
WITH (
   connector='kafka',
   properties.bootstrap.server='localhost:9092',
   topic='output',
   batch.num.messages = 1,
   primary_key = 'sum_balance'
)
FORMAT UPSERT ENCODE JSON ;
