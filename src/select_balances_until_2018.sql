DECLARE Minimum NUMERIC;
SET Minimum = 500; -- change this to your minimum balance
SELECT  wallet, transaction_hash, b.eth_balance /1000000000000000000 as EthBalance
FROM `bigquery-public-data.crypto_ethereum.balances` as b
INNER JOIN `soy-zone-369906.pubkeys_us.walets-hash` as w
ON w.wallet = b.address
WHERE  b.eth_balance /1000000000000000000 > MINIMUM
ORDER BY b.eth_balance ASC