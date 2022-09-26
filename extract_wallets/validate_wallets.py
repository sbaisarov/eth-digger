import datetime
import enum
import subprocess
import json
import os

from yaml import BlockEndToken

from wrapper import Reader, ReadAndWriteException

files = os.listdir("./cache")
if "block-number.json" not in files:
    with open("./cache/block-number.json", "w") as f:
        json.dump(40000, f)
if "wallets.json" not in files:
    with open("./cache/wallets.json", "w") as f:
        json.dump({}, f)


def call_proc():
    try:
        subprocess.run(
            f"ethereumetl export_blocks_and_transactions -w 10 \
                            --batch-size 5000 \
                            --start-block {Block.start_block} --end-block {Block.start_block + 10000} \
                            --transactions-output ./cache/transactions.csv \
                            --provider-uri https://mainnet.infura.io/v3/4f3a3997062a47bd98a80f3f965a8e89"                                                                                                         ,
            check=True,
            shell=True,
            capture_output=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}\n{e.stdout}")
        print(f"Start block number: {Block.start_block}")
        Block.cache_block_number()
        raise e


def add_wallet_and_hash(transactions_csv: Reader, old_wallets: dict):
    for transaction in transactions_csv:
        block_datetime = datetime.datetime.fromtimestamp(
            int(transaction["block_timestamp"]))
        if block_datetime.year == 2018:
            return False

        account = transaction["from_address"]
        tx_hash = transaction["hash"]
        if account in old_wallets:
            continue

        old_wallets[account] = tx_hash

    return True


def main():
    # transactions start showing up from block 40000
    with open("./cache/block-number.json", "r") as f:
        Block.start_block = json.load(f)

    with open("./cache/wallets.json", "r") as f:
        wallets: dict = json.load(f)
    try:
        extract_old_wallets(wallets)
        print(f"Finished extracting old wallets. Number of wallets: {len(wallets)}")
        extract_valid_wallets(wallets)
    finally:
        print(f"Finished extracting valid wallets. Number of wallets: {len(wallets)}")
        Block.cache_block_number()
        Block.cache_wallets(wallets)

    print("Wallets have been saved.")

def extract_old_wallets(wallets):
    while True:
        call_proc()
        transactions_csv = Reader("./cache/transactions.csv")
        result = add_wallet_and_hash(transactions_csv, wallets)
        if result == False:
            return
        print(f"Wallets with start block number {Block.start_block} and "
            f"end block number {Block.start_block + 10000} have been saved.")
        Block.start_block += 10000
        Block.cache_block_number()
        Block.cache_wallets(wallets)

def extract_valid_wallets(wallets):
    while True:
        call_proc()
        transcations_csv = Reader("./cache/transactions.csv")
        for transaction in transcations_csv:
            block_datetime = datetime.datetime.fromtimestamp(
                int(transaction["block_timestamp"]))
            if block_datetime.year < 2018:
                print("Wallets with start block number {Block.start_block} has block datetime: {block_datetime}")
                return

            account = transaction["from_address"]
            if account in wallets:
                print(f"{account} was used later than 2018: {block_datetime}")
                wallets.pop(account)
        Block.start_block += 10000
        Block.cache_block_number()
        Block.cache_wallets(wallets)


class Block(int):
    start_block = 40000


    @classmethod
    def cache_block_number(cls):
        with open("./cache/block-number.json", "w") as f:
            json.dump(cls.start_block, f)

    @classmethod
    def cache_wallets(cls, wallets):
        with open("./cache/wallets.json", "w") as f:
            json.dump(wallets, f)


main()