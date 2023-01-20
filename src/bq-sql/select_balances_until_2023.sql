DECLARE @minimum int;
DECLARE @from smallint;
DECLARE @to smallint;

SET @minimum = 10; -- change this to your minimum balance
SET @from = 2018; -- change this to your minimum year
SET @to = 2023; -- change this to your maximum year

SELECT b.address, 
  b.eth_balance /1000000000000000000 AS EthBalance, -- convert wei to ether
  MAX(t.hash) AS `hash` -- a workaround to get the hash of the last transaction.
FROM
  `bigquery-public-data.crypto_ethereum.balances` AS b
  JOIN `bigquery-public-data.crypto_ethereum.transactions`  AS t
  ON b.address = t.from_address
  WHERE
    eth_balance /1000000000000000000 >= @minimum AND
    EXTRACT(YEAR
  FROM
    t.block_timestamp) BETWEEN @from
  AND @to
GROUP BY b.address, EthBalance
ORDER BY
  EthBalance ASC