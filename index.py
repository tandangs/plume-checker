import requests

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
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for HTTP errors
        
        data = response.json()
        return {
            'tokenQualified': data.get('tokenQualified', ''),
            'claimData': data.get('claimData')
        }
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def check_wallets_from_file(file_path):
    try:
        with open(file_path, "r") as file:
            wallets = [line.strip() for line in file if line.strip()]

        results = {}
        qualified_wallets = []
        for wallet in wallets:
            print(f"Checking wallet: {wallet}")
            data = check_plume_status(wallet)
            if data and int(data.get('tokenQualified', 0)) > 0:
                qualified_wallets.append(wallet)
            results[wallet] = data

        # Save qualified wallets to a file
        with open("qualified_wallets.txt", "w") as outfile:
            outfile.write("\n".join(qualified_wallets))

        return results
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None

# Ganti dengan path ke file txt yang berisi wallet address
file_path = "wallets.txt"
results = check_wallets_from_file(file_path)

if results:
    for wallet, data in results.items():
        print(f"Wallet: {wallet}\nToken Qualified: {data.get('tokenQualified', 'N/A')}\nClaim Data: {data.get('claimData', 'N/A')}\n")
else:
    print("No results to display.")
