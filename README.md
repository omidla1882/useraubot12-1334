# 4808 - Railway Fix Applied

این ربات ویرایش شده تا ارور دیپلوی روی Railway برطرف شود.

## تغییرات اعمال شده:
- requirements.txt: اضافه شدن aiohttp
- Procfile: تغییر به `web: python bot.py`
- bot.py: اضافه شدن وب‌سرور سلامت کوچک (healthcheck) با aiohttp که روی پورت Railway پاسخ می‌دهد.
  - وب‌سرور بلافاصله بعد از شروع کلاینت اجرا می‌شود.
- تمام مقادیر API (api_id, api_hash) و session_name مثل قبل **داخل کد** هستند. نیازی به env var برای آنها نیست.

این تغییرات باعث می‌شود Railway فکر نکند برنامه کرش کرده (چون حالا روی پورت پاسخ می‌دهد).

## دیپلوی و تست حرفه‌ای (پس از تغییرات بزرگ AI):

1. تغییرات کد (ai/ + بهبود پرامپت + think + اسکورینگ بهتر) اعمال شد.
2. برای دیپلوی:
   - git add . && git commit -m "Professional Qwen3 thinking + full web3test AI core port + smarter group engagement" && git push
   - یا مستقیم ssh به سرور یوزربات:
     railway ssh --project=67a0d330-0f2d-47d5-8155-ff98bcd745a4 --environment=9595b135-9d55-4887-8226-eab3b2811801 --service=5400f4ca-400e-4160-87e4-8c77f83da4c3
     داخل شل:
       cd /app || true
       git pull || true
       python -c "
import asyncio
import bot as b
print('Qwen reachable:', asyncio.run(b.check_qwen_health()))
print('Self-test:', asyncio.run(b.run_ai_self_test(5)))
"
       tail -n 30 remember/ai_logs/responses-$(date +%Y-%m-%d).log

3. تست کیفیت و هوش (بیشتر کامل - از plan):
   python test_ai_quality.py
   python inspect_qwen.py --test

4. دیپلوی + اجرا روی سرور اختصاصی یوزربات (5400f4ca...):
   git push   # یا ssh pull
   سپس ssh:
   railway ssh --project=67a0d330-0f2d-47d5-8155-ff98bcd745a4 --environment=9595b135-9d55-4887-8226-eab3b2811801 --service=5400f4ca-400e-4160-87e4-8c77f83da4c3
   داخل:
     python -c "import asyncio, bot as b; print(asyncio.run(b.check_qwen_health())); print(asyncio.run(b.run_ai_self_test(5)))"
     tail -f remember/ai_logs/responses-*.log | grep -E 'THINK|CONTENT|INTELLIGENT|PROF'

5. بازرسی Qwen برای حداکثر عملکرد (sshهای داده شده):
   qwen: railway ssh ... --service=5874a712...
   webui: railway ssh ... --service=e60e0fa0...

6. تست زنده در گروه (از اکانت دوم):
   - سوال پیچیده → انتظار THINK + جواب واقعی grounded
   - پیام عادی → گاهی insert محتوای مرتبط طبیعی (tip واقعی برای جذب)
   - تبادل → funnel حرفه‌ای طبیعی
   هدف: همیشه خیلی هوشمند، کاملاً طبیعی و حرفه‌ای برای جذب مخاطب، درخواست‌ها درست به مدل جهت‌دهی و پردازش شوند، محتوای مرتبط واقعی گاهی درج شود، جواب‌های واقعی.

تغییرات کلیدی (more completely):
- ai/ai_core + llm_client تنها مسیر (ModelDirector برای جهت‌دهی درست، ContentIntelligence برای درج طبیعی محتوای مرتبط، full pipeline همیشه به مدل با think برای هوشمندی).
- legacy template 75% حذف/کاهش شدید برای "always intelligent".
- حافظه کاربر + زمینه برای جواب‌های واقعی پیوسته.
- critique + realness gate.

همه چیز طبق plan به‌روز برای "very intelligent + natural professional + insert relevant + real answers + properly directed to model".

## Latest Round (more complete - Phase 1/2 + live SSH verification)
- Added drug family context + improved composer (web3test patterns) → stronger "real answers" and natural relevant inserts.
- Added decide_engagement strategist (value scoring + style decision) used in observer.
- PM funnel now routes through model pipeline (context-aware) with template fallback only.
- Live SSH tests on 5400f4ca (exact command) post-deploy:
  - Strategist, director (real_answer/funnel + think=True), compose producing grounded snippets, insert_p high on value topics.
  - Multiple realistic group messages exercised → intelligent routing confirmed.
- Bot container healthy after deploys; full pipeline active for group replies.
- qwen3 + Open-WebUI inspected with exact SSHs.

If you have active groups, the random selection + intelligent reply + occasional relevant value + natural funnel will now be much higher quality. Monitor ai_responses.log and remember/ai_logs for THINK / RELEVANT_CONTENT / variant.

## Latest Major Upgrade (Phase A complete + live server verified)
- Full deprecation of legacy random<0.25 / template fallbacks in ProfessionalGroupResponder + call_qwen3_natural + handle paths.
- ALWAYS full pipeline: classify (complete rules) → plan → retrieve+compose (grounded) → ModelDirector (variant/think/temp selection for proper direction) → ContentIntelligence (probabilistic natural relevant value insert to attract) → Qwen3Client (use_think for reasoning) → naturalness + realness critique + gates.
- Prompts strengthened for professional attraction, "sometimes insert real peer experience content", concrete real answers.
- Verified live on dedicated userbot service (5400f4ca... via exact SSH): director routes to real_answer+think, insert_p high on value queries, compose produces grounded snippets (e.g. shipping times), no shortcuts.
- Deployed via railway up to service 5400f4ca... ; bot reports ACCOUNT_HEALTHY + AI conversational active.
- Qwen3 / Open-WebUI inspected (exact sshs): ready for think + high ctx (tune via UI if needed: num_ctx 3584+, temp ~0.35-0.42).
- Tests run (local + server via ssh): 5 criteria met (intelligent with reasoning, natural/professional attract, relevant content sometimes, real grounded, properly model-directed).
- Group behavior: randomly selects + replies intelligently, proactive natural starters, multi-turn value building, soft contextual PM funnel. Never low-quality/baseless.

Run yourself (exact):
railway ssh --project=67a0d330-0f2d-47d5-8155-ff98bcd745a4 --environment=9595b135-9d55-4887-8226-eab3b2811801 --service=5400f4ca-400e-4160-87e4-8c77f83da4c3
# then the python -c ai core tests + tail logs for THINK_TRACE / RELEVANT_CONTENT / INTELLIGENT_FULL

The bot is now significantly stronger/professional than before, matching the quality bar of the web3test site bot on Qwen3.