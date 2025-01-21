import requests
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

def check_plume_status(wallet_address):
    url = f"https://claim-api.plumenetwork.xyz/airdrop/credentials?walletAddress={wallet_address}"

    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.9,id;q=0.8",
        "clq-app-id": "plume",
        "dnt": "1",
        "origin": "https://claim.plumenetwork.xyz",
        "referer": "https://claim.plumenetwork.xyz/",
        "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an error for HTTP errors

        data = response.json()
        return {
            'tokenQualified': data.get('tokenQualified', ''),
            'claimData': data.get('claimData')
        }
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def read_wallets(file_path):
    try:
        with open(file_path, "r") as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []

def process_wallet(wallet, output_file):
    data = check_plume_status(wallet)
    if data and int(data.get('tokenQualified', 0)) > 0:
        with threading.Lock():
            with open(output_file, "a") as file:
                file.write(f"{wallet}, Token Qualified: {data['tokenQualified']}, Claim Data: {data['claimData']}\n")

def main():
    input_file = "wallets.txt"
    output_file = "qualified_wallets.txt"
    wallets = read_wallets(input_file)

    if not wallets:
        print("No wallets to process.")
        return

    open(output_file, "w").close()  # Clear the output file before use

    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(process_wallet, wallet, output_file): wallet for wallet in wallets}

        for future in as_completed(futures):
            wallet = futures[future]
            try:
                future.result()
            except Exception as e:
                print(f"An error occurred while processing wallet {wallet}: {e}")

if __name__ == "__main__":
    main()
