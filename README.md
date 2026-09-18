# Telegram Channel Archiver (local, personal use)

A small local web app for browsing and downloading media from Telegram
channels **you are already a member of**. It logs in as your own account
using Telegram's official API, so it only ever sees what you can already
see in the Telegram app.

## 1. Get API credentials

1. Go to https://my.telegram.org and log in with your phone number.
2. Click "API development tools".
3. Fill in any app name/platform (e.g. "My Archiver" / "Desktop").
4. Copy the `api_id` and `api_hash` you're given.

## 2. Set up the project

```bash
cd telegram-archiver
python3 -m venv venv
source venv/bin/activate      # on Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Open `config.py` and paste in your real `API_ID` and `API_HASH`.

## 3. Log in (one time)

```bash
python login.py
```

It will ask for your phone number, then the code Telegram texts/sends you,
and your 2FA password if you have one set. This creates `session.session`
— a file that keeps you logged in. **Keep it private**, it's equivalent to
being logged into your Telegram account.

## 4. Run the app

```bash
python app.py
```

Open http://127.0.0.1:5000 in your browser. You'll see a list of your
channels — click one to see its recent posts, with a Download button on
any post that has media (photo, video, file, etc.). Downloads are saved
into the `downloads/` folder.

## Notes / limits

- Only shows channels the logged-in account is already a member of —
  there's no way around that, and this app doesn't try to.
- Shows the most recent 100 posts per channel by default; edit the
  `limit=100` in `app.py` if you want more (older posts can be paged
  through with Telethon's `offset_id`, not wired up in this basic version).
- This is meant for personal use on your own machine. If you ever want to
  host it elsewhere, treat `session.session` and `config.py` as secrets.
