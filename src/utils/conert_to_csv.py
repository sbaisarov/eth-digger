import json
import csv


def convert():
    
    with open('src/extract_wallets/cache/wallets.jsonl', "r") as f:
            wallets: dict = json.load(f)

    with open("wallets.csv", "w") as f:
        csv_writer = csv.DictWriter(
            f, fieldnames=["address", "transaction_hash"])
        if f.tell() == 0:
            csv_writer.writeheader()
        
        
        for wallet, tx_hash in wallets.items():
            csv_writer.writerow({
                "address": wallet,
                "transaction_hash": tx_hash
            })


if __name__ == '__main__':
    convert()