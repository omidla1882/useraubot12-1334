#!/usr/bin/env python3
"""
Generate a fresh Telethon StringSession for Railway.

Usage (interactive):
    python3 generate_session.py

Usage (semi-automated — you still paste the OTP):
    TELEGRAM_PHONE=+98912xxxxxxx python3 generate_session.py

Then set Railway env TELETHON_SESSION_STRING=<printed string> and redeploy.
IMPORTANT: never run this session from two machines/IPs at once.
"""
import asyncio
import os
import sys
from telethon import TelegramClient
from telethon.sessions import StringSession


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
    phone = (os.environ.get('TELEGRAM_PHONE') or '').strip()
    print("Generating NEW Telethon StringSession...")
    print("Do not keep any other client online with the old session.\n")

    client = TelegramClient(StringSession(), API_ID, API_HASH)
    await client.connect()

    if not await client.is_user_authorized():
        if not phone:
            phone = input("Phone (+98...): ").strip()
        print(f"Sending code to {phone} ...")
        await client.send_code_request(phone)
        code = input("OTP code from Telegram: ").strip()
        try:
            await client.sign_in(phone=phone, code=code)
        except Exception as e:
            if 'password' in str(e).lower() or '2fa' in str(e).lower() or 'Two-steps' in str(type(e)):
                pw = input("2FA password: ").strip()
                await client.sign_in(password=pw)
            else:
                raise

    session_string = client.session.save()
    me = await client.get_me()
    await client.disconnect()

    out_path = os.environ.get('SESSION_OUT', '/tmp/telethon_session_string_new.txt')
    with open(out_path, 'w') as f:
        f.write(session_string)

    print(f"\n✅ Authenticated as: {me.first_name} (id={me.id})")
    print("\n" + "=" * 60)
    print("TELETHON_SESSION_STRING=")
    print(session_string)
    print("=" * 60)
    print(f"Also saved to: {out_path}")
    print("Set this ONLY on Railway. Do not use the same session locally afterward.")
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(asyncio.run(main()))
    except KeyboardInterrupt:
        print("\nCancelled.", file=sys.stderr)
        raise SystemExit(1)
