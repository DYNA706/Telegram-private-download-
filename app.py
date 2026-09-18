"""
Local web app to browse and download media from Telegram channels you're
already a member of.

Run `python login.py` once first to authenticate, then run this file and
open http://127.0.0.1:5000 in your browser.
"""

import os
from flask import Flask, render_template, send_file, abort
from telethon.sync import TelegramClient
from config import API_ID, API_HASH

app = Flask(__name__)

client = TelegramClient("session", API_ID, API_HASH)
client.connect()

if not client.is_user_authorized():
    raise SystemExit(
        "Not logged in yet. Run `python login.py` first, then try again."
    )

DOWNLOAD_DIR = os.path.join(os.path.dirname(__file__), "downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


@app.route("/")
def index():
    dialogs = client.get_dialogs()
    channels = [d for d in dialogs if d.is_channel]
    return render_template("index.html", channels=channels)


@app.route("/channel/<int:chat_id>")
def channel(chat_id):
    entity = client.get_entity(chat_id)
    messages = client.get_messages(entity, limit=100)
    posts = []
    for m in messages:
        if m.media or m.text:
            posts.append(
                {
                    "id": m.id,
                    "date": m.date.strftime("%Y-%m-%d %H:%M"),
                    "text": (m.text or "")[:500],
                    "has_media": bool(m.media),
                    "media_type": type(m.media).__name__ if m.media else None,
                }
            )
    return render_template(
        "channel.html", entity=entity, posts=posts, chat_id=chat_id
    )


@app.route("/download/<int:chat_id>/<int:msg_id>")
def download(chat_id, msg_id):
    entity = client.get_entity(chat_id)
    message = client.get_messages(entity, ids=msg_id)
    if not message or not message.media:
        abort(404)
    path = client.download_media(message, file=DOWNLOAD_DIR + os.sep)
    if not path:
        abort(404)
    return send_file(os.path.abspath(path), as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
