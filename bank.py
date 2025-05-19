import json
import os
from account import Account

class BankSystem:
    def __init__(self, data_file='user_data.json'):
        self.accounts = {}
        self.data_file = data_file
        self.load_data()

    def create_account(self):
        acc_no = input("Enter account number: ")
        if acc_no in self.accounts:
            print("Account already exists.")
            return
        name = input("Enter your name: ")
        password = input("Set a password: ")
        acc = Account(acc_no, name, password)
        self.accounts[acc_no] = acc
        print("Account created successfully.")

    def login(self):
        acc_no = input("Enter account number: ")
        password = input("Enter password: ")
        acc = self.accounts.get(acc_no)
        if acc and acc.password == password:
            return acc
        else:
            print("Invalid credentials.")
            return None

    def save_data(self):
        data = {
            acc_no: {
                'name': acc.name,
                'password': acc.password,
                'balance': acc.balance,
                'transactions': acc.transactions
            } for acc_no, acc in self.accounts.items()
        }
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=4)

    def load_data(self):
        if not os.path.exists(self.data_file):
            return
        with open(self.data_file, 'r') as f:
            data = json.load(f)
            for acc_no, d in data.items():
                acc = Account(acc_no, d['name'], d['password'], d['balance'])
                acc.transactions = d.get('transactions', [])
                self.accounts[acc_no] = acc
