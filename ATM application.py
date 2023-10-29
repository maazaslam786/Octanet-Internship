import json
class User:
    def __init__(self, user_id, pin):
        self.user_id = user_id
        self.pin = pin
        self.balance = 0
        self.transaction_history = []

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'pin': self.pin,
            'balance': self.balance,
            'transaction_history': self.transaction_history}

    def deposit(self, amount):
        self.balance += amount
        self.transaction_history.append(f"Deposited ${amount}")

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            self.transaction_history.append(f"Withdrew ${amount}")
        else:
            print("Insufficient balance")

    def transfer(self, to_user, amount):
        if amount <= self.balance:
            self.balance -= amount
            to_user.balance += amount
            self.transaction_history.append(f"Transferred ${amount} to User ID {to_user.user_id}")
        else:
            print("Insufficient balance")

    def display_balance(self):
        print(f"Your account balance: ${self.balance}")

    def display_transaction_history(self):
        for transaction in self.transaction_history:
            print(transaction)

class ATM:

    def __init__(self, account_file):
        self.account_file = account_file
        self.users = {}
        self.load_accounts()

    def add_user(self, user):
        self.users[user.user_id] = user
        self.save_accounts()

    def load_accounts(self):
        try:
            with open(self.account_file, 'r') as file:
                data = json.load(file)
                for user_data in data:
                    user = User(user_data['user_id'], user_data['pin'])
                    user.balance = user_data['balance']
                    user.transaction_history = user_data['transaction_history']
                    self.users[user.user_id] = user
        except FileNotFoundError:
            self.users = {}

    def save_accounts(self):
        data = [user.to_dict() for user in self.users.values()]

        with open(self.account_file, 'w') as file:
            json.dump(data, file, indent=2)

    def login(self, user_id, pin):
        if user_id in self.users and self.users[user_id].pin == pin:
            return self.users[user_id]
        else:
            return None

class ATMApplication:
    def __init__(self):
        self.atm = ATM("accounts.json")
        self.current_user = None

    def create_account(self):
        user_id = input("Enter your User ID: ")
        pin = input("Create a PIN: ")
        user = User(user_id, pin)
        self.atm.add_user(user)
        print("Account created successfully.")

    def login(self):
        user_id = input("Enter your User ID: ")
        pin = input("Enter your PIN: ")
        user = self.atm.login(user_id, pin)
        if user:
            self.current_user = user
            print("Login successful.")
        else:
            print("Login failed. Please check your User ID and PIN.")

    def main_menu(self):
        while True:
            if self.current_user is None:
                print("1. Create Account")
                print("2. Login")
                print("3. Quit")
                choice = input("Enter your choice: ")
                if choice == "1":
                    self.create_account()
                elif choice == "2":
                    self.login()
                elif choice == "3":
                    self.atm.save_accounts()  # Save accounts before quitting
                    break
                else:
                    print("Invalid choice. Please try again.")
            else:
                print("1. Deposit")
                print("2. Withdraw")
                print("3. Transfer")
                print("4. Check Balance")
                print("5. Transaction History")
                print("6. Quit")
                choice = input("Enter your choice: ")
                if choice == "1":
                    amount = float(input("Enter the amount to deposit: $"))
                    self.current_user.deposit(amount)
                elif choice == "2":
                    amount = float(input("Enter the amount to withdraw: $"))
                    self.current_user.withdraw(amount)
                elif choice == "3":
                    to_user_id = input("Enter the User ID to transfer to: ")
                    amount = float(input("Enter the amount to transfer: $"))
                    if to_user_id in self.atm.users:
                        to_user = self.atm.users[to_user_id]
                        self.current_user.transfer(to_user, amount)
                    else:
                        print("User not found.")
                elif choice == "4":
                    self.current_user.display_balance()
                elif choice == "5":
                    self.current_user.display_transaction_history()
                elif choice == "6":
                    break
                else:
                    print("Invalid choice. Please try again.")


if __name__ == "__main__":
    atm_app = ATMApplication()
    atm_app.main_menu()
