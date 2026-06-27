#!/usr/bin/env python3
"""
Run this script LOCALLY (not on Railway) to generate a fresh Telethon StringSession.
Then copy the output string into Railway as env var: TELETHON_SESSION_STRING

Usage:
    python3 generate_session.py
"""
import asyncio
import os
from telethon import TelegramClient
from telethon.sessions import StringSession

# Read from env vars. Falls back to parsing bot.py for convenience when running locally.
def _load_credentials():
    api_id = int(os.environ['TELEGRAM_API_ID']) if 'TELEGRAM_API_ID' in os.environ else 0
    api_hash = os.environ.get('TELEGRAM_API_HASH', '')
    if not api_id or not api_hash:
        try:
            with open('bot.py') as f:
                for line in f:
                    s = line.strip()
                    if s.startswith('api_id =') and not api_id:
                        api_id = int(s.split('=')[1].strip())
                    if s.startswith('api_hash =') and not api_hash:
                        api_hash = s.split('=')[1].strip().strip("'\"")
        except Exception:
            pass
    if not api_id or not api_hash:
        raise SystemExit("Set TELEGRAM_API_ID and TELEGRAM_API_HASH env vars before running.")
    return api_id, api_hash

API_ID, API_HASH = _load_credentials()


async def main():
    print("Generating new Telethon StringSession...")
    print("You will be asked for your phone number and OTP code.\n")

    async with TelegramClient(StringSession(), API_ID, API_HASH) as client:
        await client.start()
        session_string = client.session.save()
        me = await client.get_me()
        print(f"\n✅ Authenticated as: {me.first_name} (id={me.id})")
        print("\n" + "=" * 60)
        print("Copy this string and set it as Railway env var:")
        print("  Variable name:  TELETHON_SESSION_STRING")
        print("  Variable value:")
        print(session_string)
        print("=" * 60)
        print("\nThen redeploy the userbotai service on Railway.")


if __name__ == '__main__':
    asyncio.run(main())
