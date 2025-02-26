from web3 import Web3
import json

# Read config file
with open("config.json", "r") as file:
    config = json.load(file)

# Connect to Binance Smart Chain
rpc = config["blockchains"][0]["rpc"]
web3 = Web3(Web3.HTTPProvider(rpc))

# Check if connected to BSC
if not web3.isConnected():
    raise Exception("Failed to connect to Binance Smart Chain")

# Replace with your private key and recipient address
private_key = config["target_private_key"]
recipient_address = config["recipient_address"]

print(f"Tartget Private Key: {private_key}")
print(f"Recipient Address: {recipient_address}")

# Get the account address from the private key
account_address = web3.eth.account.privateKeyToAccount(private_key).address

while True :
    # Get the nonce
    nonce = web3.eth.getTransactionCount(account_address)

    # Get the balance of the account
    balance = web3.eth.get_balance(account_address)

    # Set gas price and gas limit
    gas_price = web3.eth.gas_price
    gas_limit = config["blockchains"][0]["gas_limit"]

    # Calculate the maximum amount of BNB to send (subtracting gas fees)
    max_amount = balance - (gas_price * gas_limit)

    # Create the transaction
    transaction = {
        'to': recipient_address,
        'value': max_amount,
        'gas': gas_limit,
        'gasPrice': gas_price,
        'nonce': nonce,
        'chainId': config["blockchains"][0]["chain_id"]  # BSC Mainnet chain ID
    }

    # Sign the transaction
    signed_txn = web3.eth.account.sign_transaction(transaction, private_key)

    # Send the transaction
    txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

    # Print the transaction hash
    print(f"Transaction sent with hash: {txn_hash.hex()}")