#!/usr/bin/env python3
"""
Helper to inspect/tune the Qwen3 service for maximum performance (per plan).

Usage (from your machine with railway CLI):
  python inspect_qwen.py --qwen
  python inspect_qwen.py --webui

Or run the printed ssh commands manually.

Commands are taken directly from the user-provided Railway service list.
"""

import argparse
import subprocess
import sys

QWEN_SSH = 'railway ssh --project=67a0d330-0f2d-47d5-8155-ff98bcd745a4 --environment=9595b135-9d55-4887-8226-eab3b2811801 --service=5874a712-a22c-4617-b9e5-b2464e7dac47'
WEBUI_SSH = 'railway ssh --project=67a0d330-0f2d-47d5-8155-ff98bcd745a4 --environment=9595b135-9d55-4887-8226-eab3b2811801 --service=e60e0fa0-afcf-461c-9a8d-ac025b46cc46'

def run_ssh(cmd: str, extra: str = ""):
    full = f"{cmd} {extra}".strip()
    print(f"\n>>> Running: {full}\n")
    try:
        subprocess.run(full, shell=True, check=False)
    except Exception as e:
        print("Error:", e)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--qwen', action='store_true', help='Inspect the raw qwen3 service')
    parser.add_argument('--webui', action='store_true', help='Inspect Open-WebUI (recommended for model settings & system prompt)')
    parser.add_argument('--test', action='store_true', help='Run a quick local ai core + client test')
    args = parser.parse_args()

    if args.qwen:
        print("Inspecting Qwen3 service (model list, status)...")
        run_ssh(QWEN_SSH, '"curl -s http://localhost:11434/api/tags || echo no direct curl; ps aux | grep ollama || true"')

    if args.webui:
        print("Inspecting Open-WebUI for optimal Qwen3 settings...")
        run_ssh(WEBUI_SSH, '"echo \"OpenWebUI usually on :8080 or :3000\"; curl -s http://localhost:8080/api/models || echo check UI manually"')

    if args.test:
        print("Local test of ai/ modules (no live Qwen required for logic):")
        import asyncio
        from ai.ai_core import classify_intent, retrieve_knowledge, plan_response
        from ai.llm_client import qwen3
        q = "ارسال به استانبول با USDT چقدر طول میکشه؟"
        print("Query:", q)
        print("classify:", classify_intent(q))
        print("retrieve len:", len(retrieve_knowledge(q)))
        print("plan:", plan_response(classify_intent(q), True, False, q))
        print("Client available check would call the real endpoint when bot runs.")

    if not any([args.qwen, args.webui, args.test]):
        print("Recommended commands (copy-paste):")
        print("  ", QWEN_SSH)
        print("  ", WEBUI_SSH)
        print("\nInside the shells explore:")
        print("  curl http://localhost:11434/api/tags   # for raw Ollama")
        print("  Check OpenWebUI UI for the qwen3:1.7b model parameters and any system prompt.")

if __name__ == "__main__":
    main()
