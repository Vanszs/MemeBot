import requests

url = "https://api-gw.memefi.club/graphql"
headers = {
    "Content-Type": "application/json",
    "x-apollo-operation-name": "ExploreTrendingKeyHolders",
    "Cookie": "_ga=GA1.1.1389876390.1707059026; Authentication=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7ImlkIjoiNzk3NTFjNjEtYjM1YS00YzQxLWI1MjYtYjZkNmUzYTM2ODJiIiwid2FsbGV0QWRkcmVzcyI6IjB4MDAwMDAwNGM0ZjU1NTY3NWYzMDQzZjgzYjY1MzgzNDM1OWU2NzFjMyIsImVtYWlsIjpudWxsfSwic2Vzc2lvbklkIjoiNTNkMjM2YTQtMmU2MC00ODg1LWFjMzUtYjhlNTlkYWM2NjMxIiwic3ViIjoiNzk3NTFjNjEtYjM1YS00YzQxLWI1MjYtYjZkNmUzYTM2ODJiIiwiaWF0IjoxNzA3MDU5MTI2LCJleHAiOjE3MTQ4MzUxMjZ9.2PiA9LtT4ijAI-g-shWqwcWbg3Frf8jfaeYIjFSvlk4; _ga_2GBGP137RS=GS1.1.1707059026.1.1.1707062380.0.0.0"
}

query = """
    query ExploreTrendingKeyHolders($payload: ExploreTopHoldersPayloadInput!) {
        exploreTrendingKeyHolders(payload: $payload) {
            items {
                character {
                    userId
                }
            }
        }
    }
"""

# List untuk menyimpan hasil userId dari setiap page
all_user_ids = []

# Jumlah halaman yang ingin diambil
total_pages = 200  # Ganti sesuai kebutuhan

for page in range(1, total_pages + 1):
    variables = {
        "payload": {
            "page": page,
            "limit": 100,
            "interval": "All"
        }
    }

    payload = {
        "operationName": "ExploreTrendingKeyHolders",
        "query": query,
        "variables": variables
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        result = response.json()
        data = result.get("data")
        if data:
            explore_trending_key_holders = data.get("exploreTrendingKeyHolders", {})
            items = explore_trending_key_holders.get("items", [])

            user_ids = [item["character"]["userId"] for item in items if item and item.get("character") and item["character"].get("userId")]
            all_user_ids.extend(user_ids)
        else:
            print(f"Data not found on page {page}.")
    else:
        print(f"Error on page {page}: {response.text}")

# Cetak hasil semua userId
print("All User IDs:", all_user_ids)
print(len(all_user_ids))

# Simpan list ke dalam file
with open("uset.txt", "w") as file:
    for user_id in all_user_ids:
        file.write(user_id + "\n")

print("User IDs saved to user_ids.txt")
