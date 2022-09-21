import datetime
import subprocess
import json
import os
from tkinter import W

from wrapper import Reader, ReadAndWriteException

files = os.listdir("./cache")
if "block-number.json" not in files:
    with open("block-number.json", "w") as f:
        json.dump(40000, f)
if "unselected_walllets.json" not in files:
    with open("block-unselected_walllets.json", "w") as f:
        json.dump([], f)


def call_proc(start_block, end_block):
    try:
        subprocess.run(
            f"ethereumetl export_blocks_and_transactions -w 10 \
                            --batch-size 5000 \
                            --start-block {start_block} --end-block {end_block} \
                            --transactions-output transactions.csv \
                            --provider-uri https://mainnet.infura.io/v3/4f3a3997062a47bd98a80f3f965a8e89"                                                                                                                                                                                                                                                                                                                           ,
            check=True,
            shell=True,
            capture_output=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}\n{e.stdout}")
        print(f"Start block number: {start_block}")
        with open("./cache/block-number.json", "w") as f:
            json.dump(start_block, f)
        raise e


def get_wallet_and_hash(transactions_csv: Reader, wallets: dict):
    for transaction in transactions_csv:
        block_datetime = datetime.datetime.fromtimestamp(
            int(transaction["block_timestamp"]))

        account = transaction["from_address"]
        tx_hash = transaction["transaction_hash"]
        if account in wallets:
            continue
        
        wallets[account] = tx_hash
        
        return block_datetime.year


def main():
    # transactions start showing up from block 40000
    with open("./cache/block-number.json", "r") as f:
        start_block = json.load(f)

    with open("./cache/old_wallets.json") as file:
        wallets : dict = json.load(file)
        extract_old_wallets(start_block, wallets)

    try:
        extract_valid_wallets(wallets, start_block)
    finally:
        print("Finished extracting wallets.")
        with open("verified_wallets.json") as f:
            json.dump(wallets, f)



def extract_old_wallets(start_block, wallets):
    while True:
        end_block = start_block + 50000
        # read output from csv and write to unselected_wallets.csv
        try:
            call_proc(start_block, end_block)  # ?
            transactions_csv = Reader("transactions.csv")
            year = get_wallet_and_hash(transactions_csv, wallets)
            if year == 2018:
                return
            print(f"Wallets with start block number {start_block} and "
                  f"end block number {end_block} have been saved.")
        except ReadAndWriteException as e:
            print(f"Error: {e}")
            print("Error while reading/writing to csv files.")
            raise e
        finally:
            with open("wallets.json", "w") as f:
                json.dump(wallets, f)




def extract_valid_wallets(accounts, start_block):
    while True:
        end_block = start_block + 50000
        call_proc(start_block, end_block)
        transcations_csv = Reader("transactions.csv")
        for transaction in transcations_csv:
            block_datetime = datetime.datetime.fromtimestamp(
                int(transaction["block_timestamp"]))
            if block_datetime.year < 2018:
                raise ReadAndWriteException(
                    "Blocks datetime is less than 2018.")

            account = transaction["from_address"]
            if account in accounts:
                print(f"{account} was used later than 2018: {block_datetime}")
                accounts.pop(account)


main()
