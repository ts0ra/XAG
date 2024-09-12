from src.xag import XAG
from pathlib import Path

def main():
    print("Welcome to XAG APP by ts0ra!")

    folder_path = Path('./data')
    file_path = folder_path / 'api_token.txt'
    folder_path.mkdir(parents=True, exist_ok=True)
    if not file_path.exists():
        file_path.touch()

    with open(file_path, 'r') as f:
        api_token = f.read().strip()
        if api_token:
            xag = XAG(api_token)
            xag.run()
            return

    api_token = str(input("Enter your API token: "))
    xag = XAG(api_token)
    xag.run()

if __name__ == "__main__":
    main()