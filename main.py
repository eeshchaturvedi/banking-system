from bank import BankSystem

def main():
    bank = BankSystem()
    while True:
        print("\n--- Banking Menu ---")
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")

        choice = input("Enter choice: ")
        if choice == '1':
            bank.create_account()
        elif choice == '2':
            acc = bank.login()
            if acc:
                while True:
                    print("\n1. Deposit\n2. Withdraw\n3. Balance\n4. Transactions\n5. Logout")
                    opt = input("Choice: ")
                    if opt == '1':
                        amt = float(input("Amount: "))
                        acc.deposit(amt)
                    elif opt == '2':
                        amt = float(input("Amount: "))
                        acc.withdraw(amt)
                    elif opt == '3':
                        acc.show_balance()
                    elif opt == '4':
                        acc.show_transactions()
                    elif opt == '5':
                        break
                    else:
                        print("Invalid option.")
        elif choice == '3':
            bank.save_data()
            print("Exiting. Goodbye!")
            break
        else:
            print("Invalid input.")

if __name__ == "__main__":
    main()
