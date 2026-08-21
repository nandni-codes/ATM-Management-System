# 🏧 ATM Management System

A console-based ATM Management System developed using **Python and MySQL**.

## 🚀 Features

- User Registration
- Automatic Account Number Generation
- Account Number + PIN Login
- Login Attempt Limitation
- Check Balance
- Deposit Money
- Withdraw Money
- Change PIN
- Mini Statement
- Transaction History
- Transaction Receipt
- Input Validation
- MySQL Database Integration
- Environment Variables for Database Credentials

## 🛠️ Technologies Used

- Python
- Object-Oriented Programming (OOP)
- MySQL
- MySQL Connector/Python
- python-dotenv

## 🗄️ Database

The project uses MySQL for storing account and transaction data.

### Users Table

Stores:

- Account Number
- Account Holder Name
- PIN
- Balance

### Transactions Table

Stores:

- Transaction ID
- Account Number
- Transaction Type
- Amount
- Balance After
- Transaction Time

## 🔐 Security

Database credentials are stored using environment variables through a `.env` file.

The `.env` file is excluded from Git using `.gitignore`.

## ▶️ How to Run

### 1. Clone the repository

```bash
git clone https://github.com/nandni-codes/ATM-Management-System.git
cd ATM-Management-System
```

### 2. Install Required Packages

```bash
pip install mysql-connector-python python-dotenv
```

### 3. Configure Environment Variables

Create a `.env` file in the project folder:

```env
MYSQL_HOST=localhost
MYSQL_USER=your_username
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=atm
```

> ⚠️ Do not upload your actual `.env` file or database password to GitHub.

### 4. Run the Project

```bash
python ATM.py
```

## 📸 Project Screenshots

### 📝 Registration

![Registration](screenshots/registration.png)

### ✅ Registration Successful / Account Details

![Registration Successful](screenshots/Registraction_succesful.png)

### 🔐 Login

![Login](screenshots/login.png)

### 💳 Transaction

![Transaction](screenshots/transaction.png)

### 🚪 Logout

![Logout](screenshots/logout.png)

### 👤 Users Database

![Users Table](screenshots/user_table.png)

### 💰 Transactions Database

![Transactions Table](screenshots/transaction_table.png)

## 👩‍💻 Author

**Nandni**

GitHub: [nandni-codes](https://github.com/nandni-codes)
