import datetime
import json
import csv
import sys
import logging
from hexbytes import HexBytes

import etherscan
from etherscan.errors import EtherscanIoException
import rlp
from web3 import Web3, HTTPProvider
from eth_account import Account

csv.field_size_limit(sys.maxsize)
es = etherscan.Client(api_key='5NN9FSWUYFHSTBPIMCVYDXUYNS1M4RN2PQ',
                      cache_expire_after=60)

w3 = Web3(
    HTTPProvider(
        'https://mainnet.infura.io/v3/2c4c3aed3c0548fcbbb3b8f8ee54a387'))

eth_account = Account()

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s', filename="log.txt")


def main():
    with open('src/extract_wallets/cache/wallets.json', "r") as f:
        wallets = json.load(f)
    logging.info(f"wallets loaded: {len(wallets)} wallets")

    with open("result.csv", "w") as f:
        csv_writer = csv.DictWriter(
            f, fieldnames=["address", "balance", "pubkey"])
        if f.tell() == 0:
            csv_writer.writeheader()

        write_balance_pubkey(wallets, csv_writer)


def write_balance_pubkey(wallets, csv_writer):
    with open("src/extract_wallets/cache/block-number.json", "r") as f:
        start_block = json.load(f)  # last block number of 2018

    for wallet, tx_hash in wallets.items():
        result, balance = test_wallet(wallet, start_block)
        if result == False:
            logging.info("Wallet: {} is deleted".format(wallet))
            continue

        transaction = w3.eth.get_transaction(tx_hash)
        rawTx = rlp.encode(
            [
                transaction.nonce, transaction.gasPrice, transaction.gas, HexBytes(
                    transaction.to),
                transaction.value, HexBytes(
                    transaction.input), transaction.v, transaction.r, transaction.s
            ]
        )
        public_key = Account.recover_transaction(rawTx.hex())

        logging.info(
            f"Writing to the csv file: 'address': {wallet}, 'balance': {balance}, 'pubkey': {public_key}")
        csv_writer.writerow({
            "address": wallet,
            "balance": balance,
            "pubkey": public_key
        })


def test_wallet(wallet, start_block):
    try:
        balance = w3.eth.get_balance(wallet)
    except EtherscanIoException as e:
        logging.error(f"etherscan.io error: {wallet}")

    if balance < 500:
        logging.info(
            f"Account: {wallet}, Balance: {balance} is less than 500 ETH.")
        return False, 0

    transactions = es.get_transactions_by_address(wallet,
                                                  start_block=start_block,
                                                  sort="desc",
                                                  limit=1)
    if not transactions:
        logging.info(
            "The last transaction of the account was made befeore 2018")
        return True, balance

    logging.info(f"Account: {wallet} has transactions after 2018")
    return False, 0

    # block_datetime = datetime.datetime.fromtimestamp(
    #     int(transactions["timestamp"]))
    # if block_datetime.year > 2018:
    #     logging.info(
    #         f"Account: {wallet} has transactions after 2018.\nDeleted")
    #     return None, 0


if __name__ == "__main__":
    main()
