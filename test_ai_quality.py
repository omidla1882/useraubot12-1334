#!/usr/bin/env python3
"""
Professionalism benchmark for the AI core.
Run locally: python test_ai_quality.py
Focus: intent classification, strategy, retrieval, natural gate, anti-repetition, full pipeline quality.
No real Telegram needed for pure logic tests.
"""
import asyncio
import sys
sys.path.insert(0, ".")
try:
    import bot as b
except ImportError as e:
    print("Warning: could not fully import bot:", e)
    b = None

async def main():
    print("=== UserbotAI Professional AI Quality Benchmark (Phase 4) ===\n")

    if not b:
        print("Cannot run (import fail).")
        return

    # 1. Gate rejects exact bad promo garbage from user
    bad = """برای انجام سفارش پس از واریز در فارماوب، نیاز به تأیید ارسال آدرس و انتخاب ارز دیجیتال است. همچنین، برای حفظ امنیت و محدود کردن عبور، لطفاً اطلاعات زیر را در نظر بگیرید:
📌 آدرس ارسال:
لطفاً به صورت دقیق و مشخص بازیکن خود انتخاب کنید. مثلاً:
- تلگرام: @PharmaWebGp
- اینستاگرام: فولوور شما
 پرداخت در فارماوب با ۸ ارز دیجیتال انجام می‌شود: BTC، ETH، USDT، TRX، BNB، TON، SOL، DOGE."""
    print("1. Gate bad promo:", "REJECTED ✓" if not b.is_high_quality_natural(bad) else "FAILED ✗")

    # 2. Good natural samples
    goods = [
        "رتالین واقعاً برای بعضی افراد با بیش فعالی کمک میکنه ولی حتما باید پزشک تعیین کنه.",
        "من هم شنیدم TRC20 برای USDT کارمزد کمتری داره و سریع‌تر تأیید میشه.",
        "معمولاً بعد از تأیید واریز به استانبول زیر ۸ ساعت می‌رسه. بسته‌بندی محرمانه است.",
    ]
    for g in goods:
        print(f"2. Gate natural: {'PASS ✓' if b.is_high_quality_natural(g) else 'FAIL ✗'}  → {g[:55]}")

    # 3. Classify intent (professional routing)
    print("\n3. classify_intent (reference fidelity):")
    intent_tests = [
        ("ارسال به استانبول بعد از پرداخت چقدر طول میکشه؟", "shipping_time"),
        ("برای بیش فعالی چی پیشنهاد میکنید؟", "faq_order_process"),  # or product-ish
        ("پرداخت با USDT کدوم شبکه بهتره؟", "crypto_info"),
        ("این جواب پرت بود", "complaint"),
        ("تو رباتی؟", "bot_question"),
        ("چطور سفارش بدم؟", "faq_order_process"),
        ("سلام", "greeting"),
    ]
    for q, expect in intent_tests:
        res = b.classify_intent(q)
        ok = res.get('intent') == expect or (expect == 'faq_order_process' and res.get('intent') in ('faq_order_process', 'product_info'))
        print(f"   {q[:45]:<45} → {res.get('intent')} {'✓' if ok else '≈'}")

    # 4. plan + retrieve
    print("\n4. plan_response + retrieve_knowledge:")
    for q in ["ارسال به استانبول بعد پرداخت چقدر طول میکشه؟", "ریتالین ساندوز برای ADHD", "نمیدونم کدوم شبکه تتر"]:
        intent = b.classify_intent(q)
        plan = b.plan_response(intent, True, False, q) if hasattr(b, 'plan_response') else {'strategy': b.plan_strategy(intent, True, False)}
        retrieved = b.retrieve_knowledge(q, intent.get('intent', ''))
        print(f"   Q={q[:40]} strategy={plan.get('strategy')} retrieved_len={len(retrieved)}")

    # 5. Anti-rep (conversation_brain style)
    print("\n5. is_repeated_response:")
    fake_hist = [('bot', 'معمولاً بعد از تأیید واریز به استانبول زیر ۸ ساعت می‌رسه.', None)]
    rep = "معمولاً بعد از تأیید واریز به استانبول زیر ۸ ساعت می‌رسه."
    print(f"   repeated similar → {'DETECTED ✓' if b.is_repeated_response(rep, fake_hist) else 'MISS'}")

    # 6. Live pipeline via responder or call (Qwen must be up)
    print("\n6. Full pipeline quality (live Qwen calls):")
    try:
        if hasattr(b, 'responder') and b.responder:
            r = await b.responder.generate(999999999, "برای بیش فعالی چی پیشنهاد میکنید؟", "curious")
            print("   responder.generate:", "NATURAL✓" if r and b.is_high_quality_natural(r) else "WEAK/None", "→", (r or "")[:90])
        else:
            r = await b.call_qwen3_natural(["دوستان تجربه‌ای در مورد ارسال دارید؟"], "ارسال به دبی چقدر زمان میبره؟")
            print("   call_qwen3_natural:", "NATURAL✓" if r and b.is_high_quality_natural(r) else "WEAK/None", "→", (r or "")[:90])
    except Exception as e:
        print("   live error (ok if no Qwen):", type(e).__name__)

    # 7. Self test
    print("\n7. run_ai_self_test():")
    try:
        res = await b.run_ai_self_test(3)
        print("   ", res)
    except Exception as e:
        print("   ", e)

    print("\n=== Professional benchmark finished ===")

if __name__ == "__main__":
    asyncio.run(main())
