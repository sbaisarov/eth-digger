DECLARE @minimum int;
SET @minimum = 10; -- change this to your minimum balance

SELECT  wallet, transaction_hash, -- transaction_hash is one of the transaction hashes that sent eth to an address
        b.eth_balance /1000000000000000000 as EthBalance -- convert from wei to eth
FROM `bigquery-public-data.crypto_ethereum.balances` as b
INNER JOIN `soy-zone-369906.pubkeys_us.walets-hash` as w 
ON w.wallet = b.address
WHERE  b.eth_balance /1000000000000000000 > @minimum
ORDER BY b.eth_balance ASC