import os
import textwrap
import requests
import time
from pathlib import Path

class XAG:
    def __init__(self, api_key: str):
        self.__first_run = True

        self.__api_key = api_key
        self.__base_url = "https://start-pasting.today"
        self.__API_ENDPOINTS = {
            "CHECK_STOCK": "/v2/api/stock",
            "LOGIN": "/v2/api/login",
            "SET_USERNAME": "/v2/api/set_username",
            "GENERATE": "/v2/api/generate",
            "CHECK_COIN": "/v2/api/coins",
            "CHECK_COOLDOWN": "/v2/api/cooldowns",
            "CHECK_USER_INFO": "/v2/api/get_user_info",
            "CHECK_USERNAME_TASK": "/v2/api/get_task_info",
        }

        self.__status = ""

        self.__coins = 0
        self.__balances = 0

        self.__user_id = ""
        self.__username = ""
        self.__booster = False
        self.__xag_plus = False

        self.__xag_plus_cd = 0
        self.__daily_rewards_cd = 0

        self.__xbox = 0
        self.__xbox_plus = 0
        self.__xbox_verified = 0
        self.__xbox_suspended = 0
        self.__xbox_old = 0
        self.__xgp = 0
        self.__total = 0

    def __clear(self):
        # Check the OS type and run the appropriate command
        if os.name == 'nt':
            # For Windows
            os.system('cls')
        else:
            # For macOS and Linux
            os.system('clear')

    def __response_handler(self, response: requests.Response):
        response_json = response.json()

        if (response.status_code == 200):
            self.__status = f"[{response.status_code}] Success"
        else:
            raise Exception(f"[{response.status_code}] {response_json['error']}")

        return response_json

    def __get_coins(self, timeout: int = 3):
        headers = {
            'Authorization': f'{self.__api_key}' 
        }
        
        response = requests.get(f'{self.__base_url}{self.__API_ENDPOINTS["CHECK_COIN"]}', headers=headers, timeout=timeout)
        response_json = self.__response_handler(response)
        self.__coins = response_json['coins']
        self.__balances = response_json['balance']

    def __get_user_info(self, timeout: int = 3):
        headers = {
            'Authorization': f'{self.__api_key}' 
        }

        response = requests.get(f'{self.__base_url}{self.__API_ENDPOINTS["CHECK_USER_INFO"]}', headers=headers, timeout=timeout)
        response_json = self.__response_handler(response)
        self.__user_id = response_json['user_id']
        self.__username = response_json['discord_profile']['username']
        self.__booster = response_json['is_booster']
        self.__xag_plus = response_json['has_xag_plus']

    def __get_cd(self, timeout: int = 3):
        headers = {
            'Authorization': f'{self.__api_key}' 
        }

        response = requests.get(f'{self.__base_url}{self.__API_ENDPOINTS["CHECK_COOLDOWN"]}', headers=headers, timeout=timeout)
        response_json = self.__response_handler(response)
        self.__xag_plus_cd = response_json['xag_plus_cooldown']
        self.__daily_rewards_cd = response_json['daily_reward_cooldown']

    def __get_stock(self, timeout: int = 3):
        response = requests.get(f'{self.__base_url}{self.__API_ENDPOINTS["CHECK_STOCK"]}', timeout=timeout)
        response_json = self.__response_handler(response)
        self.__xbox = response_json['xbox']
        self.__xbox_plus = response_json['xbox_plus']
        self.__xbox_verified = response_json['xbox_verified']
        self.__xbox_suspended = response_json['xbox_suspended']
        self.__xbox_old = response_json['xbox_old']
        self.__xgp = response_json['xgp']
        self.__total = response_json['total']

    def __generate(self, type, timeout: int = 10):
        if type == "":
            type = "xbox"

        headers = {
            'Authorization': f'{self.__api_key}' 
        }

        # Create a folder and a file to store the accounts (if it doesn't exist)
        print("Checking for data folder...")
        print("Checking for accounts.txt file...")
        folder_path = Path('./data')
        file_path = folder_path / 'accounts.txt'
        folder_path.mkdir(parents=True, exist_ok=True)
        if not file_path.exists():
            print("Folder and file not found!")
            print("Creating data folder and accounts.txt file...")
            file_path.touch()

        print("Generating account...")
        params = {'type': type}
        response = requests.post(f'{self.__base_url}{self.__API_ENDPOINTS["GENERATE"]}', headers=headers, timeout=timeout, params=params)
        response_json = self.__response_handler(response)

        with file_path.open('a') as file:
            detail = textwrap.dedent(f"""
            email: {response_json['account']['details']['email']}
            password: {response_json['account']['details']['password']}
            username: {response_json['account']['details']['username']['username']}
            type: {response_json['account']['details']['type']}
            used_xag_plus: {response_json['account']['used_xag_plus']}

            """)

            print("Account generated!\n")
            print(detail)

            file.write(detail)
            file.close()

    def __login(self, email: str, password: str, timeout: int = 10):
        headers = {
            'Authorization': f'{self.__api_key}' 
        }

        params = {'email': email, 'password': password}
        response = requests.post(f'{self.__base_url}{self.__API_ENDPOINTS["LOGIN"]}', headers=headers, timeout=timeout, params=params)
        response_json = self.__response_handler(response)

        print(f"\nValid: {response_json['valid']}")
        print(f"Reason: {response_json['reason']}\n")

    def __set_username(self, email: str, password: str, username: str, timeout: int = 10):
        headers = {
            'Authorization': f'{self.__api_key}' 
        }

        params = {'email': email, 'password': password, 'username': username}
        response = requests.post(f'{self.__base_url}{self.__API_ENDPOINTS["SET_USERNAME"]}', headers=headers, timeout=timeout, params=params)
        response_json = self.__response_handler(response)

        # Create a folder and a file to store the accounts (if it doesn't exist)
        print("Checking for data folder...")
        print("Checking for task_id.txt file...")
        folder_path = Path('./data')
        file_path = folder_path / 'task_id.txt'
        folder_path.mkdir(parents=True, exist_ok=True)
        if not file_path.exists():
            print("Folder and file not found!")
            print("Creating data folder and task_id.txt file...")
            file_path.touch()

        with file_path.open('a') as file:
            file.write(f"{response_json['id']}\n")
            file.close()

        print(f"\nStatus: {response_json['status']}")
        print(f"ID: {response_json['id']}\n")

    def __check_username_task(self, id: str, timeout: int = 10):
        headers = {
            'Authorization': f'{self.__api_key}' 
        }

        params = {'task_id': id}
        response = requests.get(f'{self.__base_url}{self.__API_ENDPOINTS["CHECK_USERNAME_TASK"]}', headers=headers, timeout=timeout, params=params)
        response_json = self.__response_handler(response)

        print("")
        for key, value in response_json.items():
            print(f"{key}: {value}")
        print("")

    def __refresh(self):
        try:
            print("Getting coins and balances...")
            self.__get_coins()
            print("Getting user info...")
            self.__get_user_info()
            print("Getting cooldowns...")
            self.__get_cd()
            print("Getting stocks...")
            self.__get_stock()
        except Exception as e:
            self.__status = e

    def run(self):
        while True:
            self.__clear()

            if (self.__first_run):
                self.__refresh()
                self.__first_run = False

            view = textwrap.dedent(f"""
            Welcome to XAG APP by ts0ra!
            
            =========+ INFO +=========

            Status          : {self.__status}

            Coints          : {self.__coins}
            Balances        : ${self.__balances}

            User ID         : {self.__user_id}
            Username        : {self.__username}
            Booster         : {self.__booster}
            XAG Plus        : {self.__xag_plus}

            XAG Plus CD     : {self.__xag_plus_cd}
            Daily Rewards CD: {time.strftime('%H:%M:%S', time.gmtime(self.__daily_rewards_cd))}

            =========+STOCKS+=========

            Xbox            : {self.__xbox}
            Xbox Plus       : {self.__xbox_plus}
            Xbox Verified   : {self.__xbox_verified}
            Xbox Suspended  : {self.__xbox_suspended}
            Xbox Old        : {self.__xbox_old}
            XGP             : {self.__xgp}

            TOTAL           : {self.__total}

            =========+ MENU +=========
            1. Generate
            2. Login
            3. Set Username
            4. Refresh Info and Stocks
            5. Check Username Task
            6. Exit
            """)
            print(view)

            choice = int(input("Input: "))
            match choice:
                case 1:
                    type = ""
                    while True:
                        print("Leave blank to generate default account type.")
                        type = str(input("Enter the type (xbox, xbox_plus, xbox_verified, xbox_suspended, xbox_old, xgp): "))
                        if type in ["xbox", "xbox_plus", "xbox_verified", "xbox_suspended", "xbox_old", "xgp", ""]:
                            break
                        else:
                            print("Invalid choice!")

                    try:
                        self.__generate(type)
                    except Exception as e:
                        print("")
                        print(e)
                        print("")

                    input("Press Any key to continue...")
                case 2:
                    email = str(input("Enter email: "))
                    password = str(input("Enter password: "))

                    try:
                        self.__login(email, password)
                    except Exception as e:
                        print("")
                        print(e)
                        print("")

                    input("Press Any key to continue...")
                case 3:
                    email = str(input("Enter email: "))
                    password = str(input("Enter password: "))
                    username = str(input("Enter username: "))

                    try:
                        self.__set_username(email, password, username)
                    except Exception as e:
                        print("")
                        print(e)
                        print("")

                    input("Press Any key to continue...")
                case 4:
                    print("Refreshing...")
                    self.__refresh()
                case 5:
                    id = str(input("Enter the task ID: "))
                    try:
                        self.__check_username_task(id)
                    except Exception as e:
                        print("")
                        print(e)
                        print("")

                    input("Press Any key to continue...")
                case 6:
                    break
                case _:
                    print("Invalid choice!")
                    input("Press Any key to continue...")