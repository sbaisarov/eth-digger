import datetime
import subprocess
import json
import os
import time

from wrapper import Reader

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
                            --batch-size 500 \
                            --start-block {Block.start_block} --end-block {Block.start_block + 5000} \
                            --transactions-output ./cache/transactions.csv \
                            --provider-uri https://mainnet.infura.io/v3/2c4c3aed3c0548fcbbb3b8f8ee54a387",
            check=True,
            shell=True,
            capture_output=True,
        )
        time.sleep(5)
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
        
        # seems like transaction hash belongs to the last transaction of the account
        # at the time the request was made
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
    finally:
        print(
            f"Finished extracting valid wallets. Number of wallets: {len(wallets)}"
        )
        Block.cache_block_number()
        Block.cache_wallets(wallets)
        

def extract_old_wallets(wallets):
    while True:
        call_proc()
        transactions_csv = Reader("./cache/transactions.csv")
        result = add_wallet_and_hash(transactions_csv, wallets)
        if result == False:
            print("Finished extracting old wallets until 2018.")
            return
        print(f"Wallets with start block number {Block.start_block} and "
              f"end block number {Block.start_block + 5000} have been saved.")
        Block.start_block += 5000
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

if __name__ == '__main__':
    main()