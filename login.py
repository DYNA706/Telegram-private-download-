"""
Run this once to log in to your Telegram account.
It will ask for your phone number, then the login code Telegram sends you
(and your 2FA password, if you have one enabled).

This creates a file called session.session in this folder, which stores
your logged-in session so you don't have to log in again. Keep that file
private -- anyone who has it can access your Telegram account.
"""

from telethon.sync import TelegramClient
from config import API_ID, API_HASH

def main():
    if API_ID == 12345678 or API_HASH == "your_api_hash_here":
        print("Please edit config.py first and fill in your real API_ID and API_HASH")
        print("Get them from https://my.telegram.org")
        return

    client = TelegramClient("session", API_ID, API_HASH)
    client.start()  # prompts for phone number, code, and 2FA password if needed
    me = client.get_me()
    print(f"\nLogged in as {me.first_name} (@{me.username or me.id})")
    print("You can now run: python app.py")
    client.disconnect()

if __name__ == "__main__":
    main()
