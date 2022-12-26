from src import logging
from web3 import Web3, HTTPProvider
import etherscan
from etherscan.errors import EtherscanIoException

WALLET: str = ""
START_BLOCK: int = 0
PROVIDER_API_KEY= ""
ETHERSCAN_API_KEY = ""

es = etherscan.Client(api_key="f{ETHERSCAN_API_KEY}}",
                           cache_expire_after=60)

w3 = Web3(
    HTTPProvider(
        f'https://mainnet.infura.io/v3/{PROVIDER_API_KEY}'))

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s', filename="log.txt")


def test_transactions_balance_export(wallet, start_block):
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


test_transactions_balance_export(WALLET, START_BLOCK)