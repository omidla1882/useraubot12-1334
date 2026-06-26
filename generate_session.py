#!/usr/bin/env python3
"""
Run this script LOCALLY (not on Railway) to generate a fresh Telethon StringSession.
Then copy the output string into Railway as env var: TELETHON_SESSION_STRING

Usage:
    python3 generate_session.py
"""
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession

API_ID = 23517903
API_HASH = 'f9acbac0d745902c690ecf1eaf35efbe'


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
