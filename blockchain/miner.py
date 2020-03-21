import hashlib
import requests

import sys
import pdb

from uuid import uuid4

from timeit import default_timer as timer

import random


def proof_of_work(last_proof):
    """
    Multi-Ouroboros of Work Algorithm
    - Find a number p' such that the last six digits of hash(p) are equal
    to the first six digits of hash(p')
    - IE:  last_hash: ...AE9123456, new hash 123456888...
    - p is the previous proof, and p' is the new proof
    - Use the same method to generate SHA-256 hashes as the examples in class
    """

    start = timer()

    print("Searching for proof")
    # proof = 0
    #  TODO: Your code here

    traunch = 100000
    n = 1
    proof = random.randint(0, traunch * n)
    print(f'Starting Proof\n {proof}')

    # TODO: Your code here
    while valid_proof(last_proof, proof) is False: 

        if timer() - start > 15:
            # check last proof from chain 
            CHECK_get_last_proof = get_last_proof()

            # compare local last_proof to chain last_proof
            if CHECK_get_last_proof == last_proof:
                print('👀👀👀 KEEP LOOKING 👀👀👀')
                print(f'Last Proof \n{last_proof}')
                print(f'CHECK -- last_proof on CHAIN \n{CHECK_get_last_proof}')

                # go to next traunch
                n += 1
                # pick random number
                print(f'old proof: {proof}')
                proof = random.randint(proof, (proof + (traunch * n)))
                print(f'NEW PROOF -- should be HIGHER than prev proof \n{proof}')
            else: 
                print("❌❌❌ YOU MISSED IT ❌❌❌")
                print(f'CHECK -- last_proof on CHAIN \n{CHECK_get_last_proof}')
                last_proof = get_last_proof()

                n = 1
                proof = random.randint(0, traunch * n)

            # pdb.set_trace()
            start = timer()
        else: 
            proof += 1
            # print(f"Searching for proof.... next attempt\n{proof}")

    print("Proof found: " + str(proof) + " in " + str(timer() - start))
    return proof


def valid_proof(last_proof, proof):
    """
    Validates the Proof:  Multi-ouroborus:  Do the last six characters of
    the hash of the last proof match the first six characters of the hash
    of the new proof?

    IE:  last_hash: ...AE9123456, new hash 123456E88...
    """

    # # Encode Guess
    # guess = f'{proof}'.encode()
    # # Hash Guess
    # guess_hash = hashlib.sha256(guess).hexdigest()

    # # Return True / False based on conditional
    # return last_hash[-6:] == guess_hash[:6]

    last_hash = hashlib.sha256(str(last_proof).encode()).hexdigest()
    # print(f'Last Hash: {last_hash}')
    guess = hashlib.sha256(str(proof).encode()).hexdigest()
    # print(f'Guess: {guess}')

    # if guess[:6] == last_hash[-6:]:
    #     pdb.set_trace()
    #     exit()

    return guess[:6] == last_hash[-6:]

def get_last_proof():
    r = requests.get(url=node + "/last_proof")
    data = r.json()

    return data.get('proof')


if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "https://lambda-coin.herokuapp.com/api"

    coins_mined = 0

    # Load or create ID
    f = open("my_id.txt", "r")
    id = f.read()
    print("ID is", id)
    f.close()

    if id == 'NONAME\n':
        print("ERROR: You must change your name in `my_id.txt`!")
        exit()
    # Run forever until interrupted
    while True:
        # Get the last proof from the server
        # r = requests.get(url=node + "/last_proof")
        # data = r.json()
        
        new_proof = proof_of_work(get_last_proof())

        post_data = {"proof": new_proof,
                     "id": id}

        r = requests.post(url=node + "/mine", json=post_data)
        data = r.json()
        if data.get('message') == 'New Block Forged':
            coins_mined += 1
            print('💰💰💰\n💰💰💰💰\n💰💰💰')
            print("Total coins mined: " + str(coins_mined))
            print('💰💰💰\n💰💰💰💰\n💰💰💰')
        else:
            print(data.get('message'))

        print('---END OF LOOP---')
        # pdb.set_trace()


