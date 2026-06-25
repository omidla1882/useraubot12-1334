#!/usr/bin/env python3
"""
Quick standalone test for the new natural Qwen3 behavior in the userbot.
Run with: python test_ai_quality.py
Or inside container: railway run --service userbotai python test_ai_quality.py
"""
import asyncio
import sys
sys.path.insert(0, ".")
try:
    import bot as b
except ImportError as e:
    print("Warning: could not fully import bot (missing deps like telethon):", e)
    # Still allow pure function tests if possible
    b = None

async def main():
    print("=== UserbotAI Natural Qwen3 Quality Self-Test ===\n")

    # 1. Gate test on the exact bad sample from user
    bad = """برای انجام سفارش پس از واریز در فارماوب، نیاز به تأیید ارسال آدرس و انتخاب ارز دیجیتال است. همچنین، برای حفظ امنیت و محدود کردن عبور، لطفاً اطلاعات زیر را در نظر بگیرید:
📌 آدرس ارسال:
لطفاً به صورت دقیق و مشخص بازیکن خود انتخاب کنید. مثلاً:
- تلگرام: @PharmaWebGp
- اینستاگرام: فولوور شما
 پرداخت در فارماوب با ۸ ارز دیجیتال انجام می‌شود: BTC، ETH، USDT، TRX، BNB، TON، SOL، DOGE."""
    print("1. Gate on user's bad sample:", "REJECTED ✓" if not b.is_high_quality_natural(bad) else "FAILED ✗")

    # 2. Good natural examples
    goods = [
        "رتالین واقعاً برای بعضی افراد با بیش فعالی کمک میکنه ولی حتما باید پزشک تعیین کنه.",
        "من هم شنیدم TRC20 برای USDT کارمزد کمتری داره و سریع‌تر تأیید میشه.",
    ]
    for g in goods:
        print(f"2. Gate good sample: {'PASS ✓' if b.is_high_quality_natural(g) else 'FAIL ✗'}")

    # 3. Live AI calls (requires qwen reachable inside Railway)
    print("\n3. Live natural AI calls (may take time):")
    try:
        r1 = await b.call_qwen3_natural(["دوستان کسی ریتالین ساندوز استفاده کرده؟"], "برای ADHD بزرگسال چی پیشنهاد میدین؟")
        print("   - Medical question:", "OK" if r1 and b.is_high_quality_natural(r1) else "WEAK/None", "→", (r1 or "")[:110])

        r2 = await b.call_qwen3_natural(["سلام"], "ارسال بعد پرداخت به استانبول چقدر طول میکشه؟")
        print("   - Shipping question:", "OK" if r2 and b.is_high_quality_natural(r2) else "WEAK/None", "→", (r2 or "")[:110])
    except Exception as e:
        print("   Live call error:", type(e).__name__)

    # 4. Self test helper
    print("\n4. run_ai_self_test():")
    res = await b.run_ai_self_test(3)
    print("   ", res)

    print("\n=== Test finished ===")

if __name__ == "__main__":
    asyncio.run(main())
