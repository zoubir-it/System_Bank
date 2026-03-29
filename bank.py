import hashlib 
import string
import secrets
from datetime import datetime
import time
import json 
import bcrypt





# Load JSON data from file, return empty dict if file not found
def load_data(file_name):
    try:
        with open(file_name, "r") as file:
            return json.load(file)
    
    except:
        return {}
    
# Save data into JSON file with formatting
def save_data(file_name, data):
    with open(file_name, "w") as file:
        json.dump(data, file, indent=4)

# Global constants
PASSWORD_LENGTH_WORKER = 10  # Password length for employees
MIN_PASSWORD_LENGTH_MANAGER = 10 # Password length for manager
MIN_PASSWORD_LENGTH_CLIENT = 8 # MIN Password length for client
Attempts = 3       # Max login attempts
rolldown = 30      # Rolldown period in seconds
DAILY_WITHDRAWAL_LIMIT = 2000 # Daily withdraw limit for each client


operator = {
    1 : {
        "name": "show information" ,
        "permission": True
        },
    2 : {
        "name": "edit password",
        "permission": True
    },
    3 : {
        "name": "client list",
        "permission": True
    },
    4 : {
        "name": "delete client",
        "permission": False
    },
    5 : {
        "name": "locked out client",
        "permission": False
    },
    6 : {
        "name": "show clients transactions",
        "permission": False
    }
}



        


admin_worker = {
    1 : {
        "name": "show information",
        "permission": True
        },
    2 : {
        "name": "edit password",
        "permission": True
    },
    3 : {
        "name": "client list",
        "permission": True
    },
    4 : {
        "name": "delete client",
        "permission": True
    },
    5 : {
        "name": "locked out client",
        "permission": True
    },
    6 : {
        "name": "show clients transactions",
        "permission": True
    }
}



permissions = {
    "operator": operator,
    "admin_worker": admin_worker
}



custom_permissions = load_data("permission.json")

# Generate hashed password using bcrypt
def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

class BankSystem:
    def __init__(self):
        self.manager = load_data("manager.json")
        #self.permission = load_data("permission.json")
        self.clients = Clients()  # Client management
        self.workers = Bank()     # Employee management
        self.running = True       # Main loop control
        #self.custom_permissions = {}

    

    def create_manager(self):
        
        print("=======welcome to your bank system... you have to create a manager account for your self at first, it will makes you the head and the only controller manager of the system======= ")
        first_name = input("Enter your first name: ").strip().lower()
        last_name = input("Enter your last name: ").strip().lower()
        username = f"{first_name} {last_name}"
        
        # Gender validation
        while True:
            gender = input("Enter your gender (male/female): ").lower()
            if gender in ["male", "female"]:
                break 
            print("❌ Invalid gender. Please choose male or female.")
        
    
        
        
        raw_password = input("Enter your password: ")
        
        # Password strength validation
        
        if len(raw_password) < MIN_PASSWORD_LENGTH_MANAGER \
            or not any(c in string.ascii_lowercase for c in raw_password) \
            or not any(c in string.digits for c in raw_password) \
            or not any(c in string.punctuation for c in raw_password):
            print("❌ Password rejected.")
            print("For security reasons, your password must meet the following criteria:")
            print()
            print("✔ Minimum length: 10 characters")
            print("✔ Contains letters")
            print("✔ Contains numbers")
            print("✔ Contains special characters")
            return

    #gdD9Qtpv8Z
        
        password = hash_password(raw_password)


        self.manager[username] = {
            "gender": gender,
            "password": password
        }
        save_data("manager.json", self.manager)
        #self.account_num = 1
        print("⚠️ remember your password... its your only way to get to your system")


        print("ACCOUNT CREATED SUCCESSFULLY")

        print("⚠️ its the last time your gonna see this page so you have the only account of the manger now, good luck with your system")
        
        print("⚠️ remember your password... its your only way to get to your system")

                
    
    # Handle manager login and redirect to manager area
    def manager_login(self):
        user_name = input("enter your username: ").strip().lower()
        manager = self.manager.get(user_name)
        
        if manager is None:
            print("username incorrect")
            return

        password = input("enter your password: ")

        if bcrypt.checkpw(password.encode(), manager["password"].encode()):
            print("✅login successful")
            self.manager_area()


    def show_personal_information(self):  
        """Display manager info"""
        print("========== Personal information ===========")
        for name, info in self.manager.items():
            print(f"Full name: {name}")
            print(f"Gender   : {info['gender']}")
        print("="*44)   

    def update_password(self):
        """update manager password"""
        for name, info in self.manager.items():
            pas_word = input("enter your old password: ")
            if not bcrypt.checkpw(pas_word.encode(), info["password"].encode()):
            
            
                print("wrong password, try again")
                return 
            
            raw_password = input("enter your new password: ")
            #new_password = hashlib.sha256(password.encode()).hexdigest()
            if len(raw_password) < 10 \
                or not any(c in string.ascii_lowercase for c in raw_password) \
                or not any(c in string.digits for c in raw_password) \
                or not any(c in string.punctuation for c in raw_password):
                print("❌ Password rejected.")
                print("For security reasons, your password must meet the following criteria:")
                print()
                print("✔ Minimum length: 10 characters")
                print("✔ Contains letters")
                print("✔ Contains numbers")
                print("✔ Contains special characters")
                return
            #salt = bcrypt.gensalt()
            #new_password = bcrypt.hashpw(raw_password.encode(), salt).decode()
            new_password = hash_password(raw_password)
            info['password'] = new_password
            print("✅password updated successfully ")
            save_data("manager.json", self.manager)


    # Display all registered workers with basic info        
    def show_workers_list(self):
        if len(self.workers.all_workers) == 0:
            print("there`s no employees in your bank system")
        print("{Name:<15}| {Gender:<6}|")
        for worker, info in self.workers.all_workers.items():

            print(f"{worker:<15}| {info['gender']:<6}|")
                
        

    # Delete worker from system by name
    def delete_worker(self):
        name = input("enter a name for the worker you want to delete: ").lower()
        
        if name in self.workers.all_workers:
            should_delete = input("are you sure? (y/n)").lower()
            if should_delete == "y":
                self.workers.all_workers.pop(name)
                save_data("workers.json", self.workers.all_workers)
                print("✅worker deleted successfully")
        else:
            print(f"{name} not exist in the workers list of this bank system")




    # Display permissions comparison table between operator and admin
    def show_permissions_table(self):
        operator = {
            "show information": True,
            "edit password": True,
            "client list": True,
            "delete client": False,
            "locked out client": False,
            "show clients transactions": False
        }

        admin_worker = {
            "show information": True,
            "edit password": True,
            "client list": True,
            "delete client": True,
            "locked out client": True,
            "show clients transactions": True
        }

        print("\n===================== PERMISSIONS TABLE ====================")
        print(f"{'Task':<30} | {'Operator':<10} | {'Admin Worker':<12}")
        print("-" * 60)

        for task in operator:
            op_perm = "Yes" if operator[task] else "No"
            admin_perm = "Yes" if admin_worker[task] else "No"

            print(f"{task:<30} | {op_perm:<10} | {admin_perm:<12}")

        print("=" * 60)


    
    # Assign custom permissions manually to a specific worker 
    def special_permission_worker(self):
        
        worker = input("enter a name for the worker you want to give your permission: ").lower()
        
        if worker in self.workers.all_workers:
            if worker not in custom_permissions:
                custom_permissions[worker] = {
                    "1": {"show information": None
                    },
                    "2": {"edit password": None
                    },
                    "3": {"client list": None
                    },
                    "4": {"delete client": None
                    },
                    "5": {"locked out client": None
                    },
                    "6": {"show clients transactions": None
                        }
                }
            #self.custom_permissions["name"] = worker
            for num, name in custom_permissions[worker].items():
                for task in name:
                    while True:
                        #for task in self.custom_permissions[worker]:
                            answer = input(f"{task}, (y/n): ").lower()
                            if answer in ("y", "n"):
                                custom_permissions[worker][num][task] = True if answer == "y" else False
                                break
                
                            else:
                                print("invalid option")
            self.workers.all_workers[worker]["worker_type"] = "custom"
            
            save_data("permission.json", custom_permissions)
            save_data("workers.json", self.workers.all_workers)

                            #custom_permissions[worker][task] = True if answer == "y" else False
        else:
            print(f"{worker} not exist in the workers list of this bank system")
            
                
                
    

    


    # Assign predefined permission type (operator/admin) to worker
    def permission_system(self):
        
        self.show_permissions_table()

        name = input("enter a name for the worker you want to give your permission: ").lower()
        
        if name in self.workers.all_workers:
            t_worker = input(f"enter a type of permission for {name}, (operator/admin worker): ").lower()
            if t_worker in ("operator", "admin worker"):
                if t_worker == "admin worker":
                    t_worker = t_worker.replace("admin worker", "admin_worker")
                self.workers.all_workers[name]["worker_type"] = t_worker
                save_data("workers.json", self.workers.all_workers)
                print(f"✅permission for {name} has been added successfully")
            else:
                print("invalid option")
                return
  
        else:
            print(f"{name} not exist in the workers list of this bank system")




        

    def main_menu(self):
        """Display main menu"""
        print("=============== Bank System ===============")
        print("1: Manager area")
        print("2: Client area")
        print("3: Bank area")
        print("4: Exit")
        print("=" *43)

    def manager_gateway(self):
        # Entry point for manager (login or exit)
        while True:
            print("============= Manager area ============")
            print("1: login")
            print("2: exit")
            print("="* 38)
            choice = input("enter choice: ")
            if choice == "1":
                self.manager_login()
            elif choice == "2":
                break
            else:
                print("invalid option, try again ")

    
    def manager_area(self):
        for manager, info in self.manager.items():
            title = "Mr" if info['gender'] == "male" else "Ms"
            print(f"welcome {title} {manager.title()}")
        
        while True:
            print("1: show personal information")
            print("2: edit password")
            print("3: show workers list")
            print("4: delete worker")
            print("5: permissions system")
            print("6: set each permission for worker")
            print("7: exit")
            choice = input("enter choice: ")
            if choice == "1":
                self.show_personal_information()
            elif choice == "2":
                self.update_password()
            elif choice == "3":
                self.show_workers_list()
            elif choice == "4":
                self.delete_worker()
            elif choice == "5":
                self.permission_system()
            elif choice == "6":
                self.special_permission_worker()
            elif choice == "7":
                break
            else:
                print("invalid option, try again")
    

                
            

            
    

    def client_gateway(self):
        """Client access menu"""
        while True:
            print("============= Client area =============")
            print("1: Register")
            print("2: Login")
            print("3: Exit")
            print("="* 38)
            choice = input("enter choice: ")
            if choice == "1":
                self.clients.add_client()
            elif choice == "2":
                self.clients.login()
            elif choice == "3":
                break 
            else:
                print("invalid option, try again ")
    
    def worker_gateway(self):
        """Employee access menu"""
        while True:
            print("============ workers area ============")
            print("1: Register worker")
            print("2: Login")
            print("3: Exit")
            print("=" *44)
            option = input("enter a choice: ")
            if option == "1":
                self.workers.add_user()
            elif option == "2": 
                self.workers.system_entering()
            elif option == "3":
                break 
            else:
                print("invalid option")
    
    def run(self):
        """Main system loop"""
        while self.running:
            self.main_menu()
            choice = input("enter your option: ")
            if choice == "1":
                self.manager_gateway()
            elif choice == "2":
                self.client_gateway()
            elif choice == "3":
                self.worker_gateway()
            elif choice == "4":
                print("system closed")
                self.running = False
            else:
                print("invalid choice ")
    
    def client_list(self):
        """Display all clients"""
        print(f"========= Clients List =========")
        if not self.clients.all_clients:
            print("there's no client yet") 
        print(f"{'Client':<13} | {'Gender':<6} | {'ID':<10} | {'Balance':<8}")
        print("-"*44)
        for client_id, client in self.clients.all_clients.items():
            print(f"{client['username']:<13} | {client['gender']:<6} | {client_id:<10} | {client['balance']:<8.2f}")
    
    def delete_client(self):
        """Delete a client account"""
        id_number = input("enter client ID to delete: ")
        
        if id_number in self.clients.all_clients:
            should_delete = input("are you sure? (y/n)").lower()
            if should_delete == "y":
                self.clients.all_clients.pop(id_number)
                print("✅client deleted successfully")
                save_data("clients.json", self.clients.all_clients)
                #save_data("workers.json", self.workers.all_workers)
        else:
            print("client does not exist")
            
    def locked_out(self):
        """View and unlock locked accounts"""
        if not any(client["is_locked"] for client in self.clients.all_clients.values()):
            print("there's no client acc are locked in")
            return
        
        print("========= accounts locked ==========")
        for client_id, client in self.clients.all_clients.items():
            if client["is_locked"]:
                print(f"full_name: {client['username']}")
                print(f"Client ID: {client_id}")
        print("-"*35)
        
        client_id_unlock = input("enter client id to unlock or q to quit: ")
        if client_id_unlock.lower() == "q":
            return 
        client = self.clients.all_clients.get(client_id_unlock)
        if client and client['is_locked']:
            client['is_locked'] = False 
            client['failed_attempts'] = 0
            print("✅account unlocked successfully")
            save_data("clients.json", self.clients.all_clients)
            #save_data("workers.json", self.workers.all_workers)
        else:
            print("Client not found or not locked")



    # Show last transactions of a specific client
    def show_client_transitions(self):
        client = False
        client_id = input("enter the client ID: ")
        

        for id, info in self.clients.all_clients.items():
            if client_id == id:
                client = True
                transactions = info['transactions']
                if not transactions:
                    print("No transactions for this client yet")
                    return
                
                print("Date       | Type        | Amount  | Balance")
                print("-" * 44)
                
                # Show last 5 transactions (newest first)
                for t in transactions[-5:][::-1]:
                    date = t["date"]
                    amount = t['amount']
                    balance = t['balance_after']
                    trans_type = t['trans_type']
                    
                    if trans_type in ["transfer_out", "withdraw"]:
                        print(f"{date:<10} |{trans_type:<12} | -{amount:<7} | {balance:<8}")
                    else:
                        print(f"{date:<10} |{trans_type:<12} | +{amount:<7} | {balance:<8}")
        if client == False:
            print("client not found")

    

        
        






class Bank:

    """Employee management class"""
    def __init__(self):
        self.all_workers = load_data("workers.json")  # Store all employees
        self.current_worker = None  # Currently logged in employee
        self.current_username = None


    
    # Generate random secure password for worker  
    def generate_workers_password(self):
        pass_digits = []

        characters = string.ascii_letters + string.digits
        for _ in range(PASSWORD_LENGTH_WORKER):
            pass_digits.append(secrets.choice(characters))

        return "".join(pass_digits)
    
    def generate_rolldown(self):
        '''Display rolldown timer'''
        for i in range(rolldown, 0, -1):
            print(f"00:00:{i:02}", end="\r", flush=True)
            time.sleep(1)
    
    def add_user(self):
        """Register new employee"""
        pass_digits = []
        print("========== Main System ===========")
        first_name = input("Enter your first name: ").strip()
        last_name = input("Enter your last name: ").strip()
        full_name = f"{first_name} {last_name}"
        username = full_name.lower()
        
        if username in self.all_workers:
            print("❌This employee is already registered")
            return 
        
        while True:
            gender = input("Enter your gender (male/female): ").lower()
            if gender in ["male", "female"]:
                break 
            else:
                print("❌ Invalid gender. Please choose male or female.")

        
        raw_password = self.generate_workers_password()
       
        password = hash_password(raw_password)
        self.all_workers[username.lower()] = {
            "full_name": full_name,
            "gender": gender,
            "password": password,
            "worker_type": None
        }
        save_data("workers.json", self.all_workers)
        
        print("\n" + "=" * 40)
        print("   EMPLOYEE ACCOUNT CREATED")
        print("=" * 40)
        print()
        print(f"Full Name : {username}")
        print(f"Gender    : {gender.title()}")
        print(f"Username  : {username}")
        print(f"Password  : {raw_password}")
        print()
        print("⚠️ Please keep your credentials secure.")
        print("⚠️ This password is shown only once.")
        print("=" * 40)
    
    
    
    def system_entering(self):
        """Employee login"""
        user_name = input("enter your username: ").strip().lower()
        worker = self.all_workers.get(user_name)
        
        if worker is None:
            print(f"{user_name} not found")
            return 
        
        attempt = 0
        print(f"you have {Attempts} attempts")
        
        while Attempts > attempt:
            raw_password = input("enter your password: ")
            
            if bcrypt.checkpw(raw_password.encode(), worker["password"].encode()):
                self.current_worker = worker
                self.current_username = user_name
                print("✅login successful")
                self.worker_area()
                return 
            attempt += 1
            remaining = Attempts - attempt
            print(f"wrong password, {remaining} attempts left")
        
        print("⏳ Too many attempts. Please wait.")
        self.generate_rolldown()
    
    def worker_area(self):
        global operator, admin_worker, permissions, custom_permissions


        
        """Employee dashboard"""
        title = "Mr" if self.current_worker["gender"] == "male" else "Ms"
        print(f"welcome {title} {self.current_worker['full_name'].title()}")
        
        while True:
            print("============ Main System ============")
            print("1: Show information")
            print("2: edit password ")
            print("3: Client list")
            print("4: delete client ")
            print("5: locked out client")
            print("6: show clients transactions")
            print("7: Exit ")
            
            #gdR4I3XeUh
            #if self.current_worker["worker_type"] == "operator":

            #spec_permi = custom_permissions[self.current_worker]
            #spec_permi = spec_permi.
            
            
                    
                
            worker_type = self.current_worker["worker_type"]
            if worker_type == None:
                print("you haven`t the access yet... wait for permission")
                return
            
            command_map = {
                "show information": self.show_information,
                "edit password": self.edit_password,
                "client list": system.client_list,
                "delete client": system.delete_client,
                "locked out client": system.locked_out,
                "show clients transactions": system.show_client_transitions
            }
            try:
                choice = int(input("enter your choice: "))
                if choice == 7:
                    break
                

                
                if worker_type == "custom":
                    task = custom_permissions[self.current_username].get(str(choice))
                    if task is None:
                        print("invalid option")
                        continue
                    for name, permission in task.items():
                        if permission == True:
                            command_map[name]()
                        else:
                            print("you don`t have the access to do this task")
                    
                
                else:    
                    task_type = permissions[worker_type].get(choice)
                    if task_type is None:
                        print("invalid option")
                        continue

                    if task_type["permission"] == True:
                        command_map[task_type["name"]]()
                    else:
                        print("you don`t have the access to do this task")
                    
        
            except ValueError:
        
                print("invalid option, try again") 

    def show_information(self):  
        """Display employee info"""
        print("========== Personal information ===========")
        print(f"Full name: {self.current_worker['full_name']}")
        print(f"Gender   : {self.current_worker['gender']}")
        print("="*44)
    
    def edit_password(self):
        """Change employee password"""
        pas_word = input("enter your old password: ")
        if not bcrypt.checkpw(pas_word.encode(), self.current_worker["password"].encode()):
        
        
            print("wrong password, try again")
            return 
        
        password = self.generate_workers_password()
        new_password = hash_password(password)
        self.current_worker['password'] = new_password
        print(" ✅the system generate a new password for you ")
        print(f"Your New Password:           {password} ")
        print("⚠️ Please keep your credentials secure.")
        print("⚠️ This password is shown only once.")
        save_data("workers.json", self.all_workers)



    
class Clients:
    """Client management class"""
    def __init__(self):
        self.all_clients = load_data("clients.json")  # Store all clients
        self.current_client = None  # Currently logged in client
    
    def add_client(self):
        """Register new client"""
        
        first_name = input("Enter your first name: ").strip().lower()
        last_name = input("Enter your last name: ").strip().lower()
        username = f"{first_name} {last_name}"
        
        # Gender validation
        while True:
            gender = input("Enter your gender (male/female): ").lower()
            if gender in ["male", "female"]:
                break 
            print("❌ Invalid gender. Please choose male or female.")
        
        # Password strength validation
        raw_password = input("Enter your password: ")
        if len(raw_password) < MIN_PASSWORD_LENGTH_CLIENT \
            or not any(c in string.ascii_lowercase for c in raw_password) \
            or not any(c in string.digits for c in raw_password) \
            or not any(c in string.punctuation for c in raw_password):
                print("❌ Password rejected.")
                print("For security reasons, your password must meet the following criteria:")
                print()
                print("✔ Minimum length: 8 characters")
                print("✔ Contains letters")
                print("✔ Contains numbers")
                print("✔ Contains special characters")
                return 
                
        
        password = hash_password(raw_password)
        balance = 0
        
        client_id = self._generate_client_id_()
        self.all_clients[client_id] = {
            "username": username,
            "gender": gender,
            "hash_password": password,
            "balance": balance,
            "transactions": [],
            "failed_attempts": 0,
            "daily_withdraw": 0,
            "last_withdraw" : None,  # Last withdrawal date
            "is_locked": False 
        }
        save_data("clients.json", self.all_clients)
        print("✅Account created successfully")
        print(f"Client ID: {client_id}")
        print("⚠️ Save your Client ID. It will not be shown again.")
    
    def login(self):
        """Client login"""
        client_id = input("enter Client ID: ").strip()
        client = self.all_clients.get(client_id)
        
        if client is None:
            print("❌client not found")
            return
        
        if client["is_locked"] == True:
            print("❌this account is locked")
            return 
        #z2AUpPrjyo
        # Password attempts
        while client["failed_attempts"] < 3:
            raw_password = input("enter your password: ")
            #password = hashlib.sha256(raw_password.encode()).hexdigest()
            #if client["hash_password"] == password:
            if bcrypt.checkpw(raw_password.encode(), client["hash_password"].encode()):
                self.current_client = client
                client["failed_attempts"] = 0
                self.client_area()
                return 
            
            client["failed_attempts"] += 1
            remaining = 3 - client["failed_attempts"]
            print(f"❌wrong password, you have {remaining} attempts left")
        
        client['is_locked'] = True
        print("❌ This account is locked. Contact admin.")
        
    def client_area(self):
        """Client dashboard"""
        title = "Mr" if self.current_client["gender"] == "male" else "Ms"
        print(f"welcome {title} {self.current_client['username']}")
        
        while True:
            print("\n======= Client Area =======")
            print("1: Show my information")
            print("2: deposit")
            print("3: withdraw")
            print("4: transfer")
            print("5: show transactions")
            print("6: update password ")
            print("7: Logout")

            choice = input("Choose option: ")
            if choice == "1":
                self.show_info()
            elif choice == "2":
                self.deposit()
            elif choice == "3":
                self.withdraw()
            elif choice == "4":
                self.transfer()
            elif choice == "5":
                self.show_transactions()
            elif choice == "6":
                self.edit_password()
            elif choice == "7":
                self.current_client = None
                break
            else:
                print("invalid, try again")
    
    def show_info(self):
        """Display client info"""
        print("\n====== Personal Information ======")
        print(f"Full Name : {self.current_client['username']}")
        print(f"Gender    : {self.current_client['gender'].title()}")
        print(f"Balance   : {self.current_client['balance']}$")
        print("=" * 34)
    
    def edit_password(self):
        """Change client password"""
        client = self.current_client
        raw_word = input("enter your old password: ")
        #password = hashlib.sha256(raw_word.encode()).hexdigest()
        
        #if password != client['hash_password']:
        if not bcrypt.checkpw(raw_word.encode(), self.current_client["hash_password"].encode()):
            print("❌wrong password, try again ")
            return 
        
        new_word = input("enter your password ")
        # Password strength check
        if len(new_word) < 8 \
        or not any(c in string.ascii_lowercase for c in new_word) \
        or not any(c in string.digits for c in new_word) \
        or not any(c in string.punctuation for c in new_word):
            print("❌ Weak password")
            print("Password must contain:")
            print("- At least 8 characters")
            print("- Letters")
            print("- Numbers")
            print("- Symbols")
            return
        
        
        new_password = hash_password(new_word)
        client['hash_password'] = new_password
        print("✅password updated successfully")
        save_data("clients.json", self.all_clients)
        
    def _generate_client_id_(self):
        """Generate unique client ID"""
        while True:
            client_id = "".join(secrets.choice(string.digits) for _ in range(9))
            if client_id not in self.all_clients:
                return client_id
    
    def deposit(self):
        """Deposit money"""
        try:
            amount = float(input("enter amount to deposit: "))
        except ValueError:
            print("the amount must be a number ")
            return 
        
        if amount <= 0:
            print("the amount must be positive")
            return 
        
        self.current_client['balance'] += amount
        print(f"✅the amount deposited successfully")
        print(f"your balance is {self.current_client['balance']}$")
        
        date = datetime.now().strftime("%d/%m/%Y")
        self.transaction_log(self.current_client, date, "deposit", amount, self.current_client['balance'])
        save_data("clients.json", self.all_clients)
    def withdraw(self):
        """Withdraw money with daily limit"""
        today_date = datetime.now().strftime("%d/%m/%Y")
        
        # Reset daily counter if new day
        if self.current_client['last_withdraw'] != today_date:
            self.current_client['daily_withdraw'] = 0
            
        try:
            amount = float(input("Enter amount to withdraw: "))
        except ValueError:
            print("❌ The amount must be a number.")
            return
    
        if amount <= 0:
            print("❌ The amount must be positive.")
            return
    
        if amount > self.current_client['balance']:
            print("❌ Insufficient balance.")
            return
        
        # Daily withdrawal limit check
        if self.current_client['daily_withdraw'] + amount > DAILY_WITHDRAWAL_LIMIT:
            print("❌ You can't withdraw more than 2000$ in a single day")
            return
        
        # Process withdrawal
        self.current_client['balance'] -= amount 
        self.current_client['daily_withdraw'] += amount 
        self.current_client['last_withdraw'] = today_date
        print(f"✅ You withdrew {amount}$ successfully.")
        print(f"Your current balance is {self.current_client['balance']}$")
        
        date = today_date
        self.transaction_log(self.current_client, date, "withdraw", amount, self.current_client['balance'])
        save_data("clients.json", self.all_clients)
    
    def transfer(self):
        """Transfer money to another client"""
        receiver_id = input("enter receiver Client id: ")
        receiver = self.all_clients.get(receiver_id)
        
        if receiver is None:
            print("❌receiver not found")
            return 
        
        try:
            amount = float(input("Enter amount to transfer: "))
        except ValueError:
            print("❌ The amount must be a number.")
            return
        
        if amount <= 0:
            print("❌ The amount must be positive.")
            return
        
        if amount > self.current_client['balance']:
            print("❌ Insufficient balance.")
            return
        
        # Process transfer
        self.current_client['balance'] -= amount
        date = datetime.now().strftime("%d/%m/%Y")
        
        # Log for sender
        self.transaction_log(self.current_client, date,"transfer_out", amount, self.current_client['balance'])
        
        # Log for receiver
        receiver['balance'] += amount
        self.transaction_log(receiver, date,"transfer_in", amount, receiver['balance'])
        
        print(f"✅ Successfully transferred {amount}$ to {receiver['username']}.")
        print(f"Your current balance is {self.current_client['balance']}$")
        save_data("clients.json", self.all_clients)
    
    def transaction_log(self, client, date, trans_type, amount, balance):
        """Record transaction"""
        transactions = {
            "date": date,
            "trans_type": trans_type,
            "amount": amount,
            "balance_after": balance
        }
        client["transactions"].append(transactions)
    
    def show_transactions(self):
        """Display recent transactions"""
        transactions = self.current_client['transactions']
        if not transactions:
            print("No transactions yet")
            return
        
        print("Date       | Type        | Amount  | Balance")
        print("-" * 44)
        
        # Show last 5 transactions (newest first)
        for t in transactions[-5:][::-1]:
            date = t["date"]
            amount = t['amount']
            balance = t['balance_after']
            trans_type = t['trans_type']
            
            if trans_type in ["transfer_out", "withdraw"]:
                print(f"{date:<10} |{trans_type:<12} | -{amount:<7} | {balance:<8}")
            else:
                print(f"{date:<10} |{trans_type:<12} | +{amount:<7} | {balance:<8}")


# Start the system
system = BankSystem()
while len(system.manager) == 0:
    system.create_manager()

system.run()


