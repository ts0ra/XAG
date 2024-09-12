from src.xag import XAG

def main():
    print("Welcome to XAG APP by ts0ra!")
    api_token = str(input("Enter your API token: "))
    xag = XAG(api_token)
    xag.run()

if __name__ == "__main__":
    main()