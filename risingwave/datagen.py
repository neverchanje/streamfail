#!/usr/bin/env python3
import random 
import json
import os
import sys

random.seed(42)

def transactions(max_id):
    transactions = []

    for idx in range(0,max_id):
        second = ((60 * idx) // max_id)
        delay = random.uniform(0, 10)
        from_account = random.randint(0,9)
        to_account = random.randint(0,9)
        ts = int(f'{second:02d}')

        transactions.append((second + delay, idx, { 'id': idx, 'from_account': from_account, 'to_account': to_account, 'amount': 1, 'ts': ts }))
        
    transactions.sort()
    return transactions

if __name__ == '__main__':
    
    if sys.argv[1] == "small":
        max_id = 100000
    elif sys.argv[1] == "large":
        max_id = 10000000
    else:
        print("Usage: datagen.py [small|large]")
        sys.exit(1)
    transactions = transactions(max_id)
    
    base = "transactions_small" if sys.argv[1] == "small" else "transactions_large"
    
    f = open(f'{base}.json', 'w')
    for (_, id, row) in transactions:
        print(f'{id}|{row}')
        f.write(json.dumps(row) + os.linesep)
