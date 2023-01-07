SELECT b.address, 
  (SELECT eth_balance /1000000000000000000) AS EthBalance, MAX(t.hash) AS `hash`
FROM
  `bigquery-public-data.crypto_ethereum.balances` AS b
  JOIN `bigquery-public-data.crypto_ethereum.transactions`  AS t
  ON b.address = t.from_address
  WHERE
    eth_balance /1000000000000000000 >= 10 AND
    EXTRACT(YEAR
  FROM
    t.block_timestamp) BETWEEN 2018
  AND 2023
GROUP BY b.address, EthBalance
ORDER BY
  EthBalance ASC