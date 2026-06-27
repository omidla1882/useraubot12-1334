"""
Run once locally to export session string for Railway.
Usage: python3 export_session.py
Then set TELETHON_SESSION_STRING=<output> in Railway env vars.
"""
import asyncio
import os
from telethon import TelegramClient
from telethon.sessions import StringSession

api_id = int(os.environ.get('TELEGRAM_API_ID', 0))
api_hash = os.environ.get('TELEGRAM_API_HASH', '')

if not api_id or not api_hash:
    # Fall back to reading from bot.py values if env not set (local dev only)
    try:
        import importlib.util, sys
        spec = importlib.util.spec_from_file_location("_bot", "bot.py")
        _bot = importlib.util.module_from_spec(spec)
        # Just grab the two values via grep instead of full import
        with open('bot.py') as f:
            for line in f:
                if line.strip().startswith('api_id =') and not api_id:
                    api_id = int(line.split('=')[1].strip())
                if line.strip().startswith('api_hash =') and not api_hash:
                    api_hash = line.split('=')[1].strip().strip("'\"")
    except Exception:
        pass

if not api_id or not api_hash:
    raise SystemExit("Set TELEGRAM_API_ID and TELEGRAM_API_HASH env vars before running.")


async def main():
    file_client = TelegramClient('my_session', api_id, api_hash)
    await file_client.connect()
    if not await file_client.is_user_authorized():
        print("ERROR: Session file is not authorized")
        return
    session_str = StringSession.save(file_client.session)
    await file_client.disconnect()
    print("\n=== TELETHON_SESSION_STRING ===")
    print(session_str)
    print("=== Copy the above string and set as Railway env var ===\n")


asyncio.run(main())
