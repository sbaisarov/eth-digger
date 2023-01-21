# Ethereum Public Key Extractor
## Introduction
This project is related utilizes Python and Poetry for managing the environment. The project uses BigQuery SQL queries to extract and load data from the Ethereum public dataset on Google Cloud. The goal of the project is to obtain the public keys of Ethereum wallets that have values greater than a specified amount by querying a large number of transactions.

Additionally, the project extracts hash values from transactions for each wallet and saves the data in a jsonl file. These hash values are used to retrieve full transaction data from Infura, which is then used to convert structured transaction data into raw transaction data. The raw transaction data is then used to obtain the public keys for each wallet.

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites
In order to run this project, you will need:

- Python 3.x
- Poetry
- A Google Cloud account with access to BigQuery
- An Ethereum public dataset on Google Cloud
- An Infura API key
### Installing
1. Clone or download the repository to your local machine
2. Use Poetry to create a virtual environment and install the required packages by running poetry install
3. Add your Google Cloud credentials and Infura API key to the script
4. Update the SQL query and other parameters to match your desired settings
### Running the script
Change directory to src and run the script by executing poetry run python eth-digger

## Built With
- Python - Programming language used
- Poetry - Dependency management tool
- BigQuery - SQL-like query language used to interact with the Ethereum public dataset on Google Cloud
- Infura - Ethereum blockchain infrastructure provider
## Author
Your name - Shamil Baysarov
# Acknowledgments
Thanks to https://github.com/medvedev1088 and his Ethereum public dataset on Google Cloud and Infura for making this project possible. 
