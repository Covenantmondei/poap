import os
import json
from dotenv import load_dotenv
from web3 import Web3


load_dotenv() 
w3 = Web3(Web3.HTTPProvider(os.getenv("SEPOLIA_RPC_URL"))) 
contract_address = Web3.to_checksum_address(os.getenv("CONTRACT_ADDRESS")) 
private_key = os.getenv("SEPOLIA_PRIVATE_KEY") 
account_address = w3.eth.account.privateKeyToAccount(private_key).address 
 
with open("C:\Users\Governor\Documents\poap\ABI.json") as f: 
    abi = json.load(f) 
 
contract = w3.eth.contract(address=contract_address, abi=abi) 
 
def create_event_on_chain(title, metadata, location, start_time, creator): 
    txn = contract.functions.createEvent(title, metadata, location, start_time).build_transaction({ 
        'from': account_address, 
        'nonce': w3.eth.get_transaction_count(account_address), 
        'gas': 2000000, 
        'gasPrice': w3.to_wei('50', 'gwei') 
    }) 
    signed_txn = w3.eth.account.sign_transaction(txn, private_key) 
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction) 
    return w3.to_hex(tx_hash) 

def mint_user_badge(user_address, event_id, badge_hash): 
    txn = contract.functions.mintBadge(user_address, event_id, badge_hash).build_transaction({ 
        'from': account_address, 
        'nonce': w3.eth.get_transaction_count(account_address), 
        'gas': 2000000, 
        'gasPrice': w3.to_wei('50', 'gwei') 
    }) 
    signed_txn = w3.eth.account.sign_transaction(txn, private_key) 
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction) 
    return w3.to_hex(tx_hash)