"""
Run once locally to export session string for Railway.
Usage: python3 export_session.py
Then set TELETHON_SESSION_STRING=<output> in Railway env vars.
"""
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession

api_id = 23517903
api_hash = 'f9acbac0d745902c690ecf1eaf35efbe'

async def main():
    # Read from existing file session
    file_client = TelegramClient('my_session', api_id, api_hash)
    await file_client.connect()
    if not await file_client.is_user_authorized():
        print("ERROR: Session file is not authorized")
        return
    # Export session string
    session_str = StringSession.save(file_client.session)
    await file_client.disconnect()
    print("\n=== TELETHON_SESSION_STRING ===")
    print(session_str)
    print("=== Copy the above string and set as Railway env var ===\n")

asyncio.run(main())
