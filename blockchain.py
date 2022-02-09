import hashlib
import json
import time
from turtle import st

MINING_REWARD = 10
PUZZLE_DIFFICULTY = 1


blockchain = []
open_transactions = []
owner = 'Mostafa'
participants = set()


def get_last_blockchain_value():
    """ Returns the last value of the current blockchain. """
    if len(blockchain) < 1:
        return None
    return blockchain[-1]

def valid_proof(transactions,last_hash,proof):
    block = {
        'previous_hash': last_hash,
        'index': len(blockchain),
        'transactions': transactions,
        'proof': proof
    }
    guess_hash = hash_block(block)
    print(guess_hash)
    str = ''
    return guess_hash[0:PUZZLE_DIFFICULTY] == str.zfill(PUZZLE_DIFFICULTY)


def proof_of_work():
    if len(blockchain) != 0:
        last_block = blockchain[-1]
        last_hash = hash_block(last_block)

    elif len(blockchain) == 0:
        last_hash = ''

    proof = 0
    while not valid_proof(open_transactions,last_hash,proof):
        proof += 1

    return proof 

def hash_block(block):
    return hashlib.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()


def get_balance(participant):
    tx_sender = [[tx['amount'] for tx in block['transactions']
                  if tx['sender'] == participant] for block in blockchain]
    open_tx_sender = [tx['amount'] for tx in open_transactions if tx['sender'] == participant]
    tx_sender.append(open_tx_sender)
    amount_sent = 0
    for tx in tx_sender:
        if len(tx) > 0:
            amount_sent += sum(tx)

    tx_recipient = [[tx['amount'] for tx in block['transactions']
                     if tx['recipient'] == participant] for block in blockchain]
    amount_received = 0
    for tx in tx_recipient:
        if len(tx) > 0:
            amount_received += tx[0]
    return amount_received - amount_sent


def verify_transaction(transaction):
    sender_balance = get_balance(transaction['sender'])
    return sender_balance >= transaction['amount']


def add_transaction(recipient, sender=owner, amount=1.0):

    transaction = {
        'sender': sender,
        'recipient': recipient,
        'amount': amount
    }
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(recipient)
        return True
    return False


def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    reward_transaction = {
        'sender': 'MINING',
        'recipient': owner,
        'amount': MINING_REWARD
    }
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)

    open_transactions.append(reward_transaction)
    proof = proof_of_work()

    block = {
        'previous_hash': hashed_block,
        'index': len(blockchain),
        'transactions': copied_transactions,
        'proof': proof
    }
    blockchain.append(block)
    ishash = hash_block(block)
    return True


def get_transaction_value():
    tx_recipient = input('Enter the recipient of the transaction:')
    tx_amount = float(input('Enter the amount of the transaction:'))
    return (tx_recipient, tx_amount)


def get_user_choice():
    user_input = input('Your choice: ')
    return user_input


def print_blockchain_elements():
    # Output the blockchain list to the console
    for block in blockchain:
        print('Outputting Block')
        print(block)
    else:
        print('-' * 20)


def verify_chain():
    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue
        if block['previous_hash'] != hash_block(blockchain[index-1]):
            return False
        # if not valid_proof(block['transactions'][:-1],block['previous_hash'],block['proof']):
        #     print('proof of work is invalid')
        #     return False
    return True

def verify_transactions():
    return all([verify_transaction(tx) for tx in open_transactions])

proof = proof_of_work()

gensis_block = {
    'previous_hash': '',
    'index': 0,
    'transactions': [],
    'proof': proof
}

blockchain.append(gensis_block)

waiting_for_input = True

while waiting_for_input:
    print('Please choose')
    print('1: Add a new transaction value')
    print('2: Mine a new block')
    print('3: Output the blockchain blocks')
    print('4: Output Participants')
    print('5: Verify Transactions')
    print('h: Manipulate the chain')
    print('q: Quit')
    user_choice = get_user_choice()
    if user_choice == '1':
        tx_data = get_transaction_value()
        recipient, amount = tx_data
        if add_transaction(recipient, amount=amount):
            print('Transaction Successeded')
        else:
            print('Transaction Failed!')
        print(open_transactions)
    elif user_choice == '2':
        start_mining = time.time()
        if mine_block():
            open_transactions = []
            stop_mining = time.time()
            mining_time = stop_mining - start_mining
            print(mining_time)
            if mining_time >= 5:
                PUZZLE_DIFFICULTY -= 1
            elif mining_time <= 0.2:
                PUZZLE_DIFFICULTY += 1
    elif user_choice == '3':
        print_blockchain_elements()
    elif user_choice == '4':
        print(participants)
    elif user_choice == '5':
        if verify_transaction():
            print('All transaction are valid!')
        else:
            print('There are invalid transactions')
    elif user_choice == 'h':
        if len(blockchain) >= 1:
            blockchain[0] = [2]
    elif user_choice == 'q':
        waiting_for_input = False
    else:
        print('Input was invalid, please pick a value from the list!')
    if not verify_chain():
        print_blockchain_elements()
        print('Invalid blockchain!')
        break
    print('Balance of {}: {:6.2f}'.format('Mostafa',get_balance('Mostafa')))
else:
    print('User left!')


print('Done!')
