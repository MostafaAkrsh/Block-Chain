from glob import glob
import hashlib
import json
from random import randint
import time
import datetime

MINING_REWARD = 10
PUZZLE_DIFFICULTY = 1
ATTACKER_POWER = 75

blockchain = []
open_transactions = []
owner = 'Maxwell'
participants = set()
main_blockchain = 'blockchain.txt'

def load_specific(chain):
    with open(chain,mode='r') as f:
        file_content = f.readlines()
        return json.loads(file_content[1])

def load_data():
    with open(main_blockchain,mode='r') as f:
        file_content = f.readlines()
        global blockchain
        global open_transactions
        global PUZZLE_DIFFICULTY
        blockchain = json.loads(file_content[1])
        open_transactions = json.loads(file_content[3])
        PUZZLE_DIFFICULTY = int(file_content[5])
        if len(blockchain) == 0:
            gensis_block = {
                'previous_hash': '',
                'index': 0,
                'transactions': [],
                "timestamp":str(datetime.datetime.now()),
                'proof': 0
            }
            blockchain.append(gensis_block)

load_data()

def save_data():
    with open(main_blockchain,mode='w') as f:
        f.write('blockchain\n')
        f.write(json.dumps(blockchain))
        f.write('\nopen transactions\n')
        f.write(json.dumps(open_transactions))
        f.write('\npuzzle difficulty\n')
        f.write(str(PUZZLE_DIFFICULTY))


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
        "timestamp":str(datetime.datetime.now()),
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
    return True

def verify_transactions():
    return all([verify_transaction(tx) for tx in open_transactions])



def check_longest_chain():
    chain1 = load_specific('blockchain.txt')
    chain2 = load_specific('blockchain2.txt')

    global main_blockchain
    try:
        if len(chain1) >= len(chain2):
            main_blockchain = 'blockchain.txt'
            load_data()
            return 'blockchain.txt'
        else:
            main_blockchain = 'blockchain2.txt'
            load_data()
            return 'blockchain2.txt'
    except:
        main_blockchain = 'blockchain.txt'
        return 'blockchain.txt'


def Mining_Operation():
    global PUZZLE_DIFFICULTY
    global open_transactions
    if mine_block():
        open_transactions = []
        block1 = blockchain[-1]
        block2 = blockchain[-2]
        mining_time = (datetime.datetime.strptime(block1["timestamp"], '%Y-%m-%d %H:%M:%S.%f')- datetime.datetime.strptime(block2["timestamp"], '%Y-%m-%d %H:%M:%S.%f')).total_seconds()
        print('Miningtime:' + str(mining_time))
        if mining_time >= 5:
            if PUZZLE_DIFFICULTY != 1:
                PUZZLE_DIFFICULTY -= 1
        elif mining_time <= 0.2:
            PUZZLE_DIFFICULTY += 1
        save_data()    

waiting_for_input = True

while waiting_for_input:
    check_longest_chain()
    print('Please choose')
    print('1: Add a new transaction value')
    print('2: Mine a new block')
    print('3: Output the blockchain blocks')
    print('4: Output Participants')
    print('5: Check Longest Chain')
    print('h: Manipulate the chain')
    print('l: Loop Mining')
    print('q: Quit')
    user_choice = get_user_choice()
    if user_choice == '1':
        tx_data = get_transaction_value()
        recipient, amount = tx_data
        if add_transaction(recipient, amount=amount):
            print('Transaction Successeded')
            save_data()
        else:
            print('Transaction Failed!')
        print(open_transactions)
    elif user_choice == '2':
            Mining_Operation()
    elif user_choice == '3':
        load_data()
        print_blockchain_elements()
    elif user_choice == '4':
        print(participants)
    elif user_choice == '5':
        check_longest_chain()
        print('longest chain is: '+main_blockchain)
    elif user_choice == 'h':
            attack_begin = time.time()

            if main_blockchain == 'blockchain.txt':
                main_blockchain = 'blockchain2.txt'
                attacker_block_chain = 'blockchain2.txt'
                correct_block_chain = 'blockchain.txt'
            elif main_blockchain == 'blockchain2.txt':
                main_blockchain = 'blockchain.txt'
                attacker_block_chain = 'blockchain.txt'
                correct_block_chain = 'blockchain2.txt'

            blockchain1 = blockchain
            blockchain2 = blockchain[0:-1]
            blockchain = blockchain2
            save_data()
            two_attacker_blocks_counter = 0
            while check_longest_chain() != attacker_block_chain:
                if randint(0, 100) <= ATTACKER_POWER:
                    owner = 'Maxwell'
                    main_blockchain = attacker_block_chain
                    blockchain = blockchain2
                    Mining_Operation()
                else:
                    owner = 'Mostafa'
                    main_blockchain = correct_block_chain
                    blockchain = blockchain1
                    Mining_Operation()
            attack_end = time.time()
            attack_time = attack_end - attack_begin
            print('ATTACK HAS DONE! time required:' + str(attack_time))
            owner = 'Maxwell'

    elif user_choice == 'q':
        waiting_for_input = False
    else:
        print('Input was invalid, please pick a value from the list!')
    if not verify_chain():
        print_blockchain_elements()
        print('Invalid blockchain!')
        break
    print('Balance of {}: {:6.2f}'.format(owner,get_balance(owner)))
else:
    print('User left!')


print('Done!')
