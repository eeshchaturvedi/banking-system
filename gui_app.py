import tkinter as tk
from tkinter import messagebox
from bank import BankSystem

bank = BankSystem()

class BankingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Banking System")
        self.current_account = None

        self.main_frame = tk.Frame(root)
        self.main_frame.pack(padx=20, pady=20)

        self.build_login_screen()

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def build_login_screen(self):
        self.clear_frame()
        tk.Label(self.main_frame, text="Account Number").grid(row=0, column=0)
        self.acc_entry = tk.Entry(self.main_frame)
        self.acc_entry.grid(row=0, column=1)

        tk.Label(self.main_frame, text="Password").grid(row=1, column=0)
        self.pass_entry = tk.Entry(self.main_frame, show='*')
        self.pass_entry.grid(row=1, column=1)

        tk.Button(self.main_frame, text="Login", command=self.login).grid(row=2, column=0, columnspan=2)
        tk.Button(self.main_frame, text="Create Account", command=self.build_create_screen).grid(row=3, column=0, columnspan=2)

    def build_create_screen(self):
        self.clear_frame()
        tk.Label(self.main_frame, text="Account No").grid(row=0, column=0)
        self.new_acc = tk.Entry(self.main_frame)
        self.new_acc.grid(row=0, column=1)

        tk.Label(self.main_frame, text="Name").grid(row=1, column=0)
        self.new_name = tk.Entry(self.main_frame)
        self.new_name.grid(row=1, column=1)

        tk.Label(self.main_frame, text="Password").grid(row=2, column=0)
        self.new_pass = tk.Entry(self.main_frame, show='*')
        self.new_pass.grid(row=2, column=1)

        tk.Button(self.main_frame, text="Create", command=self.create_account).grid(row=3, column=0, columnspan=2)
        tk.Button(self.main_frame, text="Back", command=self.build_login_screen).grid(row=4, column=0, columnspan=2)

    def build_dashboard(self):
        self.clear_frame()
        tk.Label(self.main_frame, text=f"Welcome {self.current_account.name}").pack()
        tk.Button(self.main_frame, text="Deposit", command=self.deposit_popup).pack()
        tk.Button(self.main_frame, text="Withdraw", command=self.withdraw_popup).pack()
        tk.Button(self.main_frame, text="Check Balance", command=self.show_balance).pack()
        tk.Button(self.main_frame, text="Logout", command=self.logout).pack()

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

    def deposit_popup(self):
        self.transaction_popup("Deposit", self.current_account.deposit)

    def withdraw_popup(self):
        self.transaction_popup("Withdraw", self.current_account.withdraw)

    def transaction_popup(self, action, func):
        def do_transaction():
            try:
                amt = float(amount_entry.get())
                func(amt)
                bank.save_data()
                messagebox.showinfo("Success", f"{action} of ₹{amt} complete.")
                win.destroy()
            except ValueError:
                messagebox.showerror("Error", "Enter a valid amount.")

        win = tk.Toplevel(self.root)
        win.title(action)
        tk.Label(win, text=f"{action} Amount").pack()
        amount_entry = tk.Entry(win)
        amount_entry.pack()
        tk.Button(win, text="Submit", command=do_transaction).pack()

    def show_balance(self):
        messagebox.showinfo("Balance", f"Your balance is ₹{self.current_account.balance}")

    def logout(self):
        self.current_account = None
        self.build_login_screen()

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = BankingApp(root)
    root.mainloop()
