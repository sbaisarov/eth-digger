import datetime
import json
import csv
import sys

import etherscan
from web3 import Web3
from web3 import eth
from eth_account import Account

csv.field_size_limit(sys.maxsize)
es = etherscan.Client(api_key='5NN9FSWUYFHSTBPIMCVYDXUYNS1M4RN2PQ',
                      cache_expire_after=60)
eth_account = Account()
# eth_api = eth.Eth(
#     Web3(
#         Web3.HTTPProvider(
#             "https://nd-430-509-576.p2pify.com/3fa3252208cd82b03008496a4fa7cd0d"
#         )))


def main():
    with open('./cache/wallets.json') as f:
        wallets = json.load(f)

    with open("result.csv", "w") as f:
        csv_writer = csv.DictWriter(
            f, fieldnames=["address", "balance", "pubkey"])
        if f.tell() == 0:
            csv_writer.writeheader()

        write_balance_pubkey(wallets, csv_writer)


def write_balance_pubkey(wallets, csv_writer):
    with open("./cache/block-number.json", "r") as f:
        start_block = json.load(f)

    for wallet, tx_hash in wallets.items():
        result, balance = test_wallet(wallet, start_block)
        if result == False:
            continue

        # response = session.get("https://etherscan.io/getRawTx?tx=" + tx_hash)
        # rawtx = re.search(r'Returned Raw Transaction Hex.*(0x.*?)\s', response.text).group(1)
        public_key = eth_api.get_transaction(tx_hash)["publicKey"]

        csv_writer.writerow({
            "address": wallet,
            "balance": balance,
            "pubkey": public_key
        })


def test_wallet(wallet, start_block):
    balance = es.get_eth_balance(wallet)
    if balance < 1000:
        print(f"Account: {wallet}, Balance: {balance} is less than 1000 ETH")
        return False, 0

    transactions = es.get_transactions_by_address(wallet,
                                                  start_block=start_block,
                                                  sort="desc",
                                                  limit=1)
    block_datetime = datetime.datetime.fromtimestamp(
        int(transactions[0]["result"]["timestamp"]))
    if block_datetime.year > 2018:
        print(f"Account: {wallet} has transactions after 2018")
        return False, 0

    return True, balance


main()
