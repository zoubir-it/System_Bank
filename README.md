Bank System

A terminal‑based banking system with multiple user roles: Manager, Workers, and Clients.

The system supports account management, transactions, permissions control, and persistent JSON storage.



Features

Manager

Create the initial manager account (only once).



View personal information and change password.



Manage workers: list, delete, assign permission types.



Set custom permissions per worker.



View all clients and their transaction history.



Delete or unlock client accounts.



Worker (Employee)

Register with an auto‑generated secure password.



Login with password attempts and temporary lockout.



Permissions can be either:



Operator – limited access.



Admin Worker – full access.



Custom – fine‑grained permissions set by the manager.



Allowed actions based on assigned permissions:



View own information.



Change own password.



List clients, delete clients, unlock clients.



View client transactions.



Client

Register with a unique 9‑digit ID.



Password must meet strength requirements (length, letters, digits, symbols).



Login with attempt limit; account locks after 3 failures.



Perform operations:



Check balance and personal information.



Deposit money.



Withdraw money (daily limit of $2000).



Transfer money to another client.



View last 5 transactions.



Change password.



Security

Passwords are hashed using bcrypt.



Workers receive random, secure passwords shown only once.



Clients choose their own strong password.



Account lockout after failed login attempts.



Daily withdrawal limit per client.



Data Persistence

All data is stored in JSON files:



manager.json



workers.json



clients.json



permission.json (custom worker permissions)



Requirements

Python 3.x



bcrypt library



Install dependencies:



bash

pip install bcrypt

How to Run

Clone the repository or download the source.



Make sure the JSON files are in the same directory (they will be created automatically if missing).



Run the script:



bash

python bank\_system.py

On first run, you will be prompted to create the manager account.



Use the menu to navigate between Manager, Client, and Worker areas.



Project Structure

text

Bank\_System/

├── bank\_system.py       # main application

├── manager.json         # manager account data

├── workers.json         # employee data

├── clients.json         # client accounts and transactions

├── permission.json      # custom worker permissions

└── README.md            # this file

Usage Example

First Run (Manager Creation)

text

=======welcome to your bank system... you have to create a manager account for your self at first, it will makes you the head and the only controller manager of the system=======

Enter your first name: John

Enter your last name: Doe

Enter your gender (male/female): male

Enter your password: strongP@ss123

ACCOUNT CREATED SUCCESSFULLY

Manager Menu Options

text

1: show personal information

2: edit password

3: show workers list

4: delete worker

5: permissions system

6: set each permission for worker

7: exit

Client Operations

Deposit, withdraw, transfer, view balance, view transaction history.



Daily withdrawal limit: $2000.



Worker Login

Workers receive a generated password upon registration.



After login, available actions depend on their permission type (Operator / Admin Worker / Custom).



Important Notes

The manager account is created only once. If manager.json exists, the creation step is skipped.



Workers cannot access the system until the manager assigns them a permission type.



Client IDs are auto‑generated and shown only once – users must save them.



Passwords are hashed with bcrypt; raw passwords are never stored.



Transactions are limited to the last 5 entries in the display, but all are saved in the JSON file.



Possible Enhancements

Add support for multiple managers.



Implement interest calculation for client balances.



Export transaction history to CSV or PDF.



Add a GUI (Tkinter or web interface).



Use a real database (SQLite) instead of JSON.



License

This project is open source and available under the MIT License.



Acknowledgements

Built with Python standard libraries and bcrypt for password hashing.



Inspired by real‑world banking system logic.



Manage your bank efficiently from the terminal.





