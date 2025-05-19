import datetime

class Account:
    def __init__(self, acc_no, name, password, balance=0):
        self.acc_no = acc_no
        self.name = name
        self.password = password
        self.balance = balance
        self.transactions = []

    def deposit(self, amount):
        self.balance += amount
        self.add_transaction("Deposit", amount)

    def withdraw(self, amount):
        if amount > self.balance:
            print("Insufficient balance.")
        else:
            self.balance -= amount
            self.add_transaction("Withdrawal", amount)

    def add_transaction(self, type_, amount):
        self.transactions.append({
            'type': type_,
            'amount': amount,
            'time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    def show_balance(self):
        print(f"Account No: {self.acc_no}, Name: {self.name}, Balance: ₹{self.balance}")

    def show_transactions(self):
        if not self.transactions:
            print("No transactions yet.")
        else:
            print("Recent Transactions:")
            for t in self.transactions[-5:]:
                print(f"{t['time']} - {t['type']}: ₹{t['amount']}")
