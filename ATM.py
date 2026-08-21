"""
ATM Management System
Developed by Nandni Wadhwa
Copyright © 2026 Nandni Wadhwa
"""

import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()
class ATM:
    def __init__(self):
        self.__pin=''
        self.balance=0
        self.name=''
        self.account_no = None
        self.login_attempts = 0
        self.main_menu()
        
    def connect_db(self):
        db = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE")
        )
        return db

    def registraction(self):
        print("\n========== REGISTRATION ==========")

        name = input("Please enter your name: ")

        while True:
            try:
                pin = int(input("Please enter a 4-digit PIN: "))

                if len(str(pin)) != 4:
                    print("PIN must be exactly 4 digits.")
                    continue

                break

            except ValueError:
                print("Please enter a valid PIN.")

        while True:
            try:
                balance = float(input("Please enter the initial balance: "))

                if balance < 0:
                    print("Balance cannot be negative.")
                    continue

                break

            except ValueError:
                print("Please enter a valid amount.")

        db = self.connect_db()
        cursor = db.cursor()

        query = """
        INSERT INTO users (name, pin, balance)
        VALUES (%s, %s, %s)
        """

        values = (name, pin, balance)

        cursor.execute(query, values)

        db.commit()

        account_no = cursor.lastrowid

        print("\n========================================")
        print("        ATM REGISTRATION RECEIPT")
        print("========================================")
        print("Account Number :", account_no)
        print("Account Holder :", name)
        print("Initial Balance: ₹", format(balance, ".2f"))
        print("----------------------------------------")
        print("Please save your Account Number.")
        print("You will need it to login.")
        print("========================================")
        print("Registration successful!")
        print("========================================\n")

        cursor.close()
        db.close()
            
    def login(self):
        print("Enter your account number")
        account_no = int(input())

        while self.login_attempts < 3:

            print("Enter your PIN")
            pin = int(input())

            db = self.connect_db()
            cursor = db.cursor()

            query = """
            SELECT account_no, name, pin, balance
            FROM users
            WHERE account_no = %s
            """

            values = (account_no,)

            cursor.execute(query, values)

            user = cursor.fetchone()

            cursor.close()
            db.close()

            if user:

                if pin == user[2]:

                    self.account_no = user[0]
                    self.name = user[1]
                    self.__pin = user[2]
                    self.balance = float(user[3])

                    self.login_attempts = 0

                    print("\nLogin successful!")
                    print("Welcome", self.name)

                    self.atm_menu()
                    return

                else:
                    self.login_attempts += 1
                    remaining = 3 - self.login_attempts

                    if remaining > 0:
                        print("Incorrect PIN")
                        print("Attempts remaining:", remaining)
                    else:
                        print("Account temporarily locked!")

            else:
                print("Account not found!")
                return
        
    def set_pin(self):
        print("Enter your old PIN")
        old_pin = int(input())

        if old_pin != self.__pin:
            print("Incorrect old PIN")
            self.atm_menu()
            return

        print("Enter your new PIN")
        new_pin = int(input())

        if new_pin == old_pin:
            print("New PIN cannot be the same as old PIN")
            self.atm_menu()
            return

        if len(str(new_pin)) != 4:
            print("PIN must be exactly 4 digits")
            self.atm_menu()
            return

        db = self.connect_db()
        cursor = db.cursor()

        query = """
        UPDATE users
        SET pin = %s
        WHERE account_no = %s
        """

        cursor.execute(query, (new_pin, self.account_no))

        db.commit()

        self.__pin = new_pin

        print("PIN changed successfully!")

        cursor.close()
        db.close()

        self.atm_menu()
    def get_amount(self, message):
        while True:
            try:
                amount = float(input(message))

                if amount <= 0:
                    print("Please enter a positive amount.")
                    continue

                return amount

            except ValueError:
                print("Please enter a valid number.")
            
    def atm_menu(self):
        print("\n========== ATM MENU ==========")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Change PIN")
        print("4. Mini Statement")
        print("5. Check Balance")
        print("6. Logout")
        print("==============================")

        try:
            num = int(input("Enter your choice: "))

            if num == 1:
                self.deposit()

            elif num == 2:
                self.withdraw()

            elif num == 3:
                self.set_pin()

            elif num == 4:
                self.mini_statement()

            elif num == 5:
                self.check_balance()

            elif num == 6:
                print("Logout successful!")
                return

            else:
                print("Please enter a number between 1 and 6.")
                self.atm_menu()

        except ValueError:
            print("Invalid input! Please enter a number.")
            self.atm_menu()
    def main_menu(self):
        print("Enter 'r' for the registraction")
        print("Enter 'l' for the login")
        user_input=input()
        if(user_input=='r'):
            self.registraction()
        elif(user_input=='l'):
            self.login()
        else:
            exit()  
        
    def withdraw(self):
        withdraw_amt = self.get_amount("Enter the withdrawal amount: ")

        if withdraw_amt > self.balance:
            print("Insufficient balance.")
        else:
            self.balance = self.balance - withdraw_amt

            db = self.connect_db()
            cursor = db.cursor()

            query = """
            UPDATE users
            SET balance = %s
            WHERE account_no = %s
            """

            cursor.execute(query, (self.balance, self.account_no))

            query = """
            INSERT INTO transactions
            (account_no, transaction_type, amount, balance_after)
            VALUES (%s, %s, %s, %s)
            """

            cursor.execute(
                query,
                (self.account_no, "WITHDRAW", withdraw_amt, self.balance)
            )

            db.commit()

            print("Withdrawal successful!")
            print("Withdrawn amount:", withdraw_amt)
            print("Current balance:", self.balance)
            self.show_receipt("WITHDRAW", withdraw_amt)

            cursor.close()
            db.close()

            self.atm_menu()
    def deposit(self):
        dep_amt = self.get_amount("Enter the deposit amount: ")

        self.balance = self.balance + dep_amt

        db = self.connect_db()
        cursor = db.cursor()

        query = """
        UPDATE users
        SET balance = %s
        WHERE account_no = %s
        """

        cursor.execute(query, (self.balance, self.account_no))

        query = """
        INSERT INTO transactions
        (account_no, transaction_type, amount, balance_after)
        VALUES (%s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (self.account_no, "DEPOSIT", dep_amt, self.balance)
        )

        db.commit()

        print("Deposit successful!")
        print("Deposited amount:", dep_amt)
        print("Current balance:", self.balance)
        self.show_receipt("DEPOSIT", dep_amt)

        cursor.close()
        db.close()

        self.atm_menu()
        
    def check_balance(self):
        db = self.connect_db()
        cursor = db.cursor()

        query = """
        SELECT name, balance
        FROM users
        WHERE account_no = %s
        """

        cursor.execute(query, (self.account_no,))

        user = cursor.fetchone()

        if user:
            self.name = user[0]
            self.balance = float(user[1])

            print("\n========== ACCOUNT BALANCE ==========")
            print("Account Number:", self.account_no)
            print("Account Holder:", self.name)
            print("Current Balance: ₹", self.balance)
            print("=====================================\n")

        else:
            print("Account not found.")

        cursor.close()
        db.close()

        self.atm_menu()
        
    def show_receipt(self, transaction_type, amount):
        print("\n========================================")
        print("         ATM TRANSACTION RECEIPT")
        print("========================================")
        print("Account Number :", self.account_no)
        print("Account Holder :", self.name)
        print("Transaction    :", transaction_type)
        print("Amount         : ₹", format(amount, ".2f"))
        print("Balance After  : ₹", format(self.balance, ".2f"))
        print("Status         : SUCCESS")
        print("========================================\n")
            
    def mini_statement(self):
        db = self.connect_db()
        cursor = db.cursor()

        query = """
        SELECT transaction_type, amount, balance_after, transaction_time
        FROM transactions
        WHERE account_no = %s
        ORDER BY transaction_time DESC
        """

        values = (self.account_no,)

        cursor.execute(query, values)

        transactions = cursor.fetchall()

        print("\n========== MINI STATEMENT ==========")

        if not transactions:
            print("No transactions found.")

        else:
            for transaction in transactions:
                print("------------------------------------")
                print("Type:", transaction[0])
                print("Amount:", transaction[1])
                print("Balance:", transaction[2])
                print("Date:", transaction[3])

        print("====================================\n")

        cursor.close()
        db.close()

        self.atm_menu()

obj=ATM()

