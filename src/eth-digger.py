import json
import csv
import sys
import logging

from eth_account import Account
from csv_wrapper import Reader, Writer, ReadAndWriteException

from hexbytes import HexBytes
import etherscan
import rlp
from web3 import Web3, HTTPProvider

INFURA_API_KEY = ""
ETHERSCAN_API_KEY = ""


csv.field_size_limit(sys.maxsize)  # curent field size limit is not enough for some rows
es = etherscan.Client(api_key=f'{ETHERSCAN_API_KEY}',
                      cache_expire_after=60)

w3 = Web3(
    HTTPProvider(
        f"https://mainnet.infura.io/v3/{INFURA_API_KEY}")

eth_account = Account()

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s', filename="log.txt")
logging.info("HTTP provider - Infura")


def main():
    wallet_balance = Reader("src/storage/wallet_balance.csv",
                                    ["wallet", "transaction_hash", "EthBalance"])
    logging.info(f"wallets loaded: {len(wallet_balance)} wallets")

    result = Writer("result.csv", ["wallet", "EthBalance", "pubkey"])
    try:
        eval_pubkey(wallet_balance, result)
    except ReadAndWriteException:
        print(ReadAndWriteException)
    finally:
        wallet_balance.close()
        result.close()


def eval_pubkey(wallet_balance, result):
    # with open("src/extract_wallets/cache/block-number.json", "r") as f:
    #     start_block = json.load(f)  # last block number of 2018

    for row in wallet_balance:
        wallet = row["wallet"]
        tx_hash = row["transaction_hash"]
        balance = row["EthBalance"]
        # if result == False:
        #     logging.info("Wallet: {} is deleted".format(wallet))
        #     continue

        transaction = w3.eth.get_transaction(tx_hash)
        receipent = transaction.to
        if receipent is None:  # might be null
            continue
        rawTx = rlp.encode(
            [
                transaction.nonce, transaction.gasPrice, transaction.gas, HexBytes(
                    transaction.to),
                transaction.value, HexBytes(
                    transaction.input), transaction.v, transaction.r, transaction.s
            ]
        )
        public_key = Account.recover_transaction(rawTx.hex())

        result.writerow({
            "wallet": wallet,
            "EthBalance": balance,
            "pubkey": public_key
        })
        logging.info(
            f"Row added: 'address': {wallet}, 'balance': {balance}, 'pubkey': {public_key}")


main()
