import threading
import requests
from web3 import Web3

# node w3
w3 = Web3(Web3.HTTPProvider('')) # your link node web3 (infura, etc)

# enter your info
walletOwner = Web3.to_checksum_address('') # your wallet
walletRecipient = Web3.to_checksum_address('') # wallet recipient
privateKey = '' # private key for your wallet

# enter fee and minimal summary to sweep
ETH_GAS = w3.to_wei(40, 'gwei') # 40 to wei
ETH_MIN = w3.to_wei(0.002, 'ether') # 0.002 to wei

# optional
requests.get('https://api.telegram.org/bot/sendMessage?chat_id=&text=Crashed watcher activated.')

# loop
def loop():
    while True:
        balance = w3.eth.get_balance(walletOwner) # get balance
        nonce = w3.eth.get_transaction_count(walletOwner) # get count transaction
        summ = balance - ETH_GAS * 21000 # all cash from wallet
        tx = {
            'nonce': nonce,
            'to': walletRecipient,
            'value': summ,
            'gas': 21000,
            'gasPrice': ETH_GAS
        }
        print(f'Balance: {balance}')
        try:
            if balance > ETH_MIN:
                signedTx = w3.eth.account.sign_transaction(tx, privateKey) # sign transaction
                txHash = w3.eth.send_raw_transaction(signedTx.rawTransaction) # send transaction to blockchain
                print(w3.to_hex(txHash))
        except:
            print('Api error, watch next')


threading.Thread(target=loop(), daemon=True).start()
input('Enter exit')
