import json
import csv
import re

import etherscan
from web3 import Web3
from web3 import eth
from eth_account import Account

es = etherscan.Client(api_key='5NN9FSWUYFHSTBPIMCVYDXUYNS1M4RN2PQ',
                      cache_expire_after=60)
eth_account = Account()


def main():
    with open('./cache/wallets.json') as f:
        wallets = json.load(f)

    with open("result.csv", "w") as f:
        csv_writer = csv.DictWriter(
            f, fieldnames=["address", "balance", "pubkey"])
        if f.tell() == 0:
            csv_writer.writeheader()

        write_balance_pubkey(wallets, csv_writer)


def write_balance_pubkey(accounts, csv_writer):
    eth_api = eth.Eth(
        Web3(
            Web3.HTTPProvider(
                "https://nd-430-509-576.p2pify.com/3fa3252208cd82b03008496a4fa7cd0d"
            )))
    for account, tx_hash in accounts.items():
        balance = es.get_eth_balance(account)
        if balance < 1000:
            print(
                f"Account: {account}, Balance: {balance} is less than 1000 ETH"
            )
            continue
        # response = session.get("https://etherscan.io/getRawTx?tx=" + tx_hash)
        # rawtx = re.search(r'Returned Raw Transaction Hex.*(0x.*?)\s', response.text).group(1)
        public_key = eth_api.get_transaction(tx_hash)["publicKey"]
        csv_writer.writerow({
            "address": account,
            "balance": balance,
            "pubkey": public_key
        })


main()
