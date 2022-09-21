import json
import csv

import etherscan
from hexbytes import HexBytes
import requests
import web3
from web3.eth import Eth
from eth_typing.evm import Hash32

es = etherscan.Client(api_key='5NN9FSWUYFHSTBPIMCVYDXUYNS1M4RN2PQ',
                      cache_expire_after=60)
# w3 = web3.Web3(web3.HTTPProvider('https://mainnet.infura.io/v3/4f3a3997062a47bd98a80f3f965a8e89'))

def main():
    with open('wallets.json') as f:
        wallets = json.load(f)

    with open("result.csv", "a+") as f:
        csv_writer = csv.DictWriter(f, fieldnames=["address", "balance", "pubkey"])
        if f.tell() == 0:
            csv_writer.writeheader()

        write_balance_pubkey(wallets, csv_writer)


def write_balance_pubkey(accounts, csv_writer):
    session = requests.Session()
    for account, tx_hash in accounts.items():
        balance = es.get_eth_balance(account)
        if balance > 1000:
            print(f"Account: {account}, Balance: {balance} has more than 1000 ETH")
        rawtx = session.get("https://etherscan.io/getRawTx?tx=0x" + tx_hash)
        pubkey = account.recover_transaction(rawtx)
        csv_writer.writerow({"address": account, "balance": balance, "pubkey": pubkey})


main()

# s = w3.eth.account._keys.Signature(vrs=(
#     to_standard_v(extract_chain_id(tx.v)[1]),
#     w3.toInt(tx.r),
#     w3.toInt(tx.s)
# ))

# print("signature: ", s)

# from eth_account._utils.legacy_transactions import ALLOWED_TRANSACTION_KEYS
# tt = {k:tx[k] for k in ALLOWED_TRANSACTION_KEYS - {'chainId', 'data'}}
# tt['data']=tx.input
# tt['chainId']=extract_chain_id(tx.v)[0]

# print("Transaction: ", tt)

# from eth_account._utils.legacy_transactions import serializable_unsigned_transaction_from_dict
# ut = serializable_unsigned_transaction_from_dict(tt)

# print("Hash:: ", ut.hash())

# print("Public kye: ", s.recover_public_key_from_msg_hash(ut.hash()))