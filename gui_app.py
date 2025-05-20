import tkinter as tk
from tkinter import messagebox
from bank import BankSystem

bank = BankSystem()

class BankingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Banking System")
        self.root.geometry("400x400")
        self.root.resizable(False, False)
        self.current_account = None

        self.main_frame = tk.Frame(root, bg="#f4f4f4")
        self.main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        self.build_login_screen()

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def style_label(self, text):
        return tk.Label(self.main_frame, text=text, font=("Arial", 12), bg="#f4f4f4")

    def style_entry(self):
        return tk.Entry(self.main_frame, font=("Arial", 12), width=25)

    def style_button(self, text, command):
        return tk.Button(self.main_frame, text=text, command=command, font=("Arial", 11), bg="#4CAF50", fg="white", width=22, pady=5)

    def build_login_screen(self):
        self.clear_frame()
        tk.Label(self.main_frame, text="Login", font=("Arial", 16, "bold"), bg="#f4f4f4").pack(pady=10)

        self.style_label("Account Number").pack(pady=5)
        self.acc_entry = self.style_entry()
        self.acc_entry.pack()

        self.style_label("Password").pack(pady=5)
        self.pass_entry = self.style_entry()
        self.pass_entry.config(show='*')
        self.pass_entry.pack()

        self.style_button("Login", self.login).pack(pady=10)
        self.style_button("Create Account", self.build_create_screen).pack()

    def build_create_screen(self):
        self.clear_frame()
        tk.Label(self.main_frame, text="Create Account", font=("Arial", 16, "bold"), bg="#f4f4f4").pack(pady=10)

        self.style_label("Account Number").pack(pady=5)
        self.new_acc = self.style_entry()
        self.new_acc.pack()

        self.style_label("Name").pack(pady=5)
        self.new_name = self.style_entry()
        self.new_name.pack()

        self.style_label("Password").pack(pady=5)
        self.new_pass = self.style_entry()
        self.new_pass.config(show='*')
        self.new_pass.pack()

        self.style_button("Create", self.create_account).pack(pady=10)
        self.style_button("Back", self.build_login_screen).pack()

    def build_dashboard(self):
        self.clear_frame()
        tk.Label(self.main_frame, text=f"Welcome, {self.current_account.name}", font=("Arial", 16, "bold"), bg="#f4f4f4").pack(pady=10)

        actions = [
            ("Deposit", self.deposit_popup),
            ("Withdraw", self.withdraw_popup),
            ("Check Balance", self.show_balance),
            ("Transaction History", self.show_transactions),
            ("Logout", self.logout)
        ]

        for text, cmd in actions:
            self.style_button(text, cmd).pack(pady=5)

    def create_account(self):
        acc_no = self.new_acc.get()
        name = self.new_name.get()
        password = self.new_pass.get()
        if acc_no and name and password:
            if acc_no in bank.accounts:
                messagebox.showerror("Error", "Account already exists.")
            else:
                from account import Account
                bank.accounts[acc_no] = Account(acc_no, name, password)
                bank.save_data()
                messagebox.showinfo("Success", "Account created.")
                self.build_login_screen()
        else:
            messagebox.showerror("Error", "Please fill all fields.")

    def login(self):
        acc_no = self.acc_entry.get()
        password = self.pass_entry.get()
        acc = bank.accounts.get(acc_no)
        if acc and acc.password == password:
            self.current_account = acc
            self.build_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials.")

    def transaction_popup(self, action, func):
        def do_transaction():
            try:
                amt = float(amount_entry.get())
                func(amt)
                bank.save_data()
                messagebox.showinfo("Success", f"{action} of ₹{amt} successful.")
                win.destroy()
            except ValueError:
                messagebox.showerror("Error", "Enter a valid amount.")

        win = tk.Toplevel(self.root)
        win.title(action)
        win.geometry("300x150")
        win.resizable(False, False)

        tk.Label(win, text=f"{action} Amount", font=("Arial", 12)).pack(pady=10)
        amount_entry = tk.Entry(win, font=("Arial", 12))
        amount_entry.pack(pady=5)
        tk.Button(win, text="Submit", command=do_transaction, font=("Arial", 11), bg="#4CAF50", fg="white").pack(pady=10)

    def deposit_popup(self):
        self.transaction_popup("Deposit", self.current_account.deposit)

    def withdraw_popup(self):
        self.transaction_popup("Withdraw", self.current_account.withdraw)

    def show_balance(self):
        messagebox.showinfo("Balance", f"Your balance is ₹{self.current_account.balance:.2f}")

    def show_transactions(self):
        win = tk.Toplevel(self.root)
        win.title("Transaction History")
        win.geometry("400x250")
        win.resizable(False, False)

        tk.Label(win, text="Last 5 Transactions", font=("Arial", 14, "bold")).pack(pady=10)
        transactions = self.current_account.transactions[-5:]
        if not transactions:
            tk.Label(win, text="No transactions yet.", font=("Arial", 12)).pack()
        else:
            for t in transactions:
                line = f"{t['time']} | {t['type']} | ₹{t['amount']}"
                tk.Label(win, text=line, anchor="w", justify="left", font=("Arial", 11)).pack(fill="x", padx=20)

    def logout(self):
        self.current_account = None
        self.build_login_screen()

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = BankingApp(root)
    root.mainloop()
