import random


class Account:
    def __init__(self, name, email, address, account_type):
        self.name = name
        self.email = email
        self.address = address
        self.account_type = account_type
        self.balance = 0
        self.account_number = random.randint(10000, 99999)
        self.transaction_history = []
        self.loan_count = 0

    def deposit(self, amount):
        self.balance += amount
        self.transaction_history.append(('Deposit', amount))

    def withdraw(self, amount):
        if amount > self.balance:
            return "Withdrawal amount exceeded"
        self.balance -= amount
        self.transaction_history.append(('Withdraw', amount))

    def check_balance(self):
        return self.balance

    def get_transaction_history(self):
        return self.transaction_history

    def take_loan(self, amount):
        if self.loan_count < 2:
            self.balance += amount
            self.loan_count += 1
            self.transaction_history.append(('Loan', amount))
        else:
            return "Loan limit reached"

    def transfer(self, amount, recipient_account):
        if amount > self.balance:
            return "Insufficient funds"
        if recipient_account:
            self.withdraw(amount)
            recipient_account.deposit(amount)
            return "Transfer successful"
        else:
            return "Account does not exist"


class Bank:
    def __init__(self):
        self.accounts = {}
        self.total_loans = 0
        self.loan_feature = True

    def create_account(self, name, email, address, account_type):
        new_account = Account(name, email, address, account_type)
        self.accounts[new_account.account_number] = new_account
        return new_account.account_number

    def delete_account(self, account_number):
        if account_number in self.accounts:
            del self.accounts[account_number]
            return "Account deleted"
        else:
            return "Account does not exist"

    def list_accounts(self):
        return [(acc.account_number, acc.name, "Savings" if acc.account_type == 1 else "Current") for acc in self.accounts.values()]

    def total_balance(self):
        return sum(acc.balance for acc in self.accounts.values())

    def toggle_loan_feature(self):
        self.loan_feature = not self.loan_feature
        return "Loan feature turned " + ("on" if self.loan_feature else "off")


class Admin:
    def __init__(self, bank):
        self.bank = bank

    def create_user_account(self, name, email, address, account_type):
        return self.bank.create_account(name, email, address, account_type)

    def delete_user_account(self, account_number):
        return self.bank.delete_account(account_number)

    def view_all_accounts(self):
        return self.bank.list_accounts()

    def check_bank_balance(self):
        return self.bank.total_balance()

    def check_total_loans(self):
        return self.bank.total_loans

    def manage_loan_feature(self):
        return self.bank.toggle_loan_feature()


def main():
    bank = Bank()
    admin = Admin(bank)
    while True:

        user_input = int(
            input(" 1. User\n 2. Admin\n 3. Exit\n Choose an option: "))
        if user_input == 1:
            action = int(input(
                "\n 1. Create account\n 2. Deposite\n 3. Withdraw\n 4. Check Balance\n 5. Take Loan\n 6. Transfer\n 7. Exit\n Choose an option: "))
            if action == 1:
                name = input("Enter your name: ")
                email = input("Enter your email: ")
                address = input("Enter your address: ")
                account_type = int(
                    input("\t1. Savings \n\t2. Current\n\tAccount Type: "))
                account_number = admin.create_user_account(
                    name, email, address, account_type)
                print(f"Account created with number: {account_number}")

            elif action == 2:
                account_number = int(input("Enter your account number: "))
                amount = int(input("Enter amount to deposit: "))
                account = bank.accounts.get(account_number)
                if account:
                    account.deposit(amount)
                    print("Amount deposited")
                else:
                    print("Account does not exist")

            elif action == 3:
                account_number = int(input("Enter your account number: "))
                amount = int(input("Enter amount to withdraw: "))
                account = bank.accounts.get(account_number)
                if account:
                    response = account.withdraw(amount)
                    print(response)
                else:
                    print("Account does not exist")

            elif action == 4:
                account_number = int(input("Enter your account number: "))
                account = bank.accounts.get(account_number)
                if account:
                    print(f"Your balance is {account.check_balance()}")
                else:
                    print("Account does not exist")

            elif action == 5:
                account_number = int(input("Enter your account number: "))
                amount = int(input("Enter amount to take as loan: "))
                account = bank.accounts.get(account_number)

                if not bank.loan_feature:
                    print("Loan feature is currently off")
                    return

                if account:
                    response = account.take_loan(amount)
                    print(response)

                else:
                    print("Account does not exist")

            elif action == 6:
                account_number = int(input("Enter your account number: "))
                recipient_account_number = int(
                    input("Enter recipient account number: "))
                amount = int(input("Enter amount to transfer: "))
                account = bank.accounts.get(account_number)
                recipient_account = bank.accounts.get(recipient_account_number)

                if account and recipient_account:
                    response = account.transfer(amount, recipient_account)
                    print(response)
                else:
                    print("Account does not exist")

            elif action == 7:
                break

            else:
                print("Invalid input\n")

        elif user_input == 2:

            action = int(input(
                "\n 1. Create\n 2. Delete\n 3. List Accounts\n 4. Total Balance\n 5. Manage Loans\n 6. Exit\n Choose an option: "))

            if action == 1:
                name = input("Enter user name: ")
                email = input("Enter user email: ")
                address = input("Enter user address: ")
                account_type = int(
                    input("\t1. Savings \n\t2. Current\n\tAccount Type: "))
                account_number = admin.create_user_account(
                    name, email, address, account_type)
                print(f"Account created with number: {account_number}")

            elif action == 2:
                account_number = int(input("Enter account number to delete: "))
                print(admin.delete_user_account(account_number))

            elif action == 3:
                accounts = admin.view_all_accounts()
                for acc in accounts:
                    print(f"Account Number: {acc[0]}, Name: {
                          acc[1]}, Account Type: {acc[2]}")

            elif action == 4:
                total_balance = admin.check_bank_balance()
                print(f"Total Bank Balance: {total_balance}")

            elif action == 5:
                print(admin.manage_loan_feature())

            elif action == 6:
                break
            else:
                print("Invalid input\n")

        elif user_input == 3:
            break

        else:
            print("Invalid input\n")


main()
