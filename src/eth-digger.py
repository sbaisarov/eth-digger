import logging
import os

from hexbytes import HexBytes
import dotenv
from eth_account import Account
import rlp
from web3 import Web3, HTTPProvider

from fileio import csv
from fileio import jsonl
from fileio.exceptions import ReadAndWriteException


dotenv.load_dotenv()
input_file = os.getenv("INPUT_FILE")
if input_file == None:
    raise ReadAndWriteException("INPUT_FILE is not defined")

output_file = os.getenv("OUTPUT_FILE")
if output_file is None:
    output_file = "result.csv"

INPUT_FILE = os.path.join(os.path.dirname(__file__), f"fileio/data/{input_file}")
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), f"fileio/data/{output_file}")

w3 = Web3(HTTPProvider(f"https://mainnet.infura.io/v3/{os.getenv('INFURA_API_KEY')}"))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="log.txt",
)
logging.info("HTTP provider - Infura")


def main():
    if INPUT_FILE.endswith(".csv"):
        reader = csv.Reader(INPUT_FILE, ["address", "hash", "EthBalance"])
    elif INPUT_FILE.endswith(".jsonl"):
        reader = jsonl.Reader(INPUT_FILE)
        # result = jsonl.Writer(OUTPUT_FILE)  # not implemented yet
    else:
        raise ReadAndWriteException("File format not supported")

    result = csv.Writer(OUTPUT_FILE, ["address", "EthBalance", "pubkey"])
    logging.info(f"wallets loaded: {len(reader)} wallets")

    try:
        eval_pubkey(reader, result)
    except ReadAndWriteException as e:
        print(e)
    finally:
        reader.close()
        result.close()


def eval_pubkey(wallet_balance, result: csv.Writer):
    already_processed = result.to_address_list("address")
    for row in wallet_balance:
        wallet = row["address"]
        if wallet in already_processed:
            continue
        tx_hash = row["hash"]  # last transacton hash
        balance = row["EthBalance"]  # current balance

        transaction = w3.eth.get_transaction(tx_hash)
        receipent = transaction.to
        if receipent is None:  # might be null
            continue
        rawTx = rlp.encode(
            [
                transaction.nonce,
                transaction.gasPrice,
                transaction.gas,
                HexBytes(transaction.to),
                transaction.value,
                HexBytes(transaction.input),
                transaction.v,
                transaction.r,
                transaction.s,
            ]
        )
        public_key = Account.recover_transaction(rawTx.hex())

        result.writerow(
            {"address": wallet, "EthBalance": balance, "pubkey": public_key}
        )
        # the public key generated for this address(wallet)
        logging.info(
            f"Row added: 'address': {wallet}, 'balance': {balance}, 'Public key': {public_key}"
        )


main()
