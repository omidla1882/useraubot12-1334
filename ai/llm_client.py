"""
Async LLM client for userbotai — optimized for qwen3:1.7b.
Supports think=true for internal reasoning (professional feature).
Uses aiohttp to match the rest of the Telethon bot.
"""

import asyncio
import os
import re
from typing import Dict, List, Optional, Tuple

import aiohttp

# Simple semaphore to protect the small model on CPU
_inference_sem = asyncio.Semaphore(int(os.getenv('CHAT_AI_MAX_CONCURRENT', '2')))


def _parse_think_blocks(text: str) -> Tuple[str, str]:
    """Return (thinking_text, final_text). Strips <think>...</think>."""
    if not text:
        return "", ""
    # Capture thinking
    think_match = re.search(r'<think>([\s\S]*?)</think>', text, re.IGNORECASE)
    thinking = think_match.group(1).strip() if think_match else ""
    # Remove all think blocks
    final = re.sub(r'<think>[\s\S]*?</think>', '', text, flags=re.IGNORECASE)
    final = re.sub(r'</?think[^>]*>', '', final, flags=re.IGNORECASE).strip()
    return thinking, final


class Qwen3Client:
    """Async client with explicit thinking support for intelligent Qwen3 responses."""

    def __init__(self):
        self.base_url = os.getenv(
            'QWEN3_BASE_URL',
            os.getenv('OLLAMA_BASE_URL', 'http://qwen3.railway.internal:11434'),
        ).rstrip('/')
        self.model = os.getenv('QWEN3_MODEL', os.getenv('OLLAMA_MODEL', 'qwen3:1.7b'))
        self.timeout = float(os.getenv('QWEN3_TIMEOUT', '90'))
        self.default_max_tokens = int(os.getenv('QWEN3_MAX_TOKENS', '340'))
        self.default_temperature = float(os.getenv('QWEN3_TEMPERATURE', '0.44'))
        self.default_num_ctx = int(os.getenv('QWEN3_NUM_CTX', '4096'))

    async def is_available(self) -> bool:
        try:
            timeout = aiohttp.ClientTimeout(total=8)
            async with aiohttp.ClientSession(timeout=timeout) as sess:
                async with sess.get(f"{self.base_url}/api/tags") as resp:
                    data = await resp.json(content_type=None)
                    models = [m.get('name', '') for m in data.get('models', [])]
                    return any(self.model.split(':')[0] in m for m in models) or bool(models)
        except Exception:
            return False

    async def chat(
        self,
        messages: List[Dict[str, str]],
        *,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        use_think: bool = False,
        num_ctx: int = 3584,
    ) -> Dict:
        """
        Send chat. If use_think=True we ask for reasoning trace (internal intelligence).
        Returns dict with 'content', 'thinking', 'raw', 'model', 'time'.
        """
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "think": bool(use_think),
            "options": {
                "temperature": temperature if temperature is not None else self.default_temperature,
                "num_predict": max_tokens or self.default_max_tokens,
                "num_ctx": num_ctx or self.default_num_ctx,
                "top_p": 0.88,
                "top_k": 45,
                "repeat_penalty": 1.12,
                "repeat_last_n": 64,
                "presence_penalty": 0.08,
                "frequency_penalty": 0.05,
                "num_thread": int(os.getenv('QWEN3_NUM_THREAD', '4')),
            },
        }

        start = asyncio.get_event_loop().time()
        async with _inference_sem:
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            async with aiohttp.ClientSession(timeout=timeout) as sess:
                async with sess.post(f"{self.base_url}/api/chat", json=payload) as r:
                    if r.status != 200:
                        raise RuntimeError(f"Qwen3 chat failed: {r.status}")
                    data = await r.json(content_type=None)

        elapsed = asyncio.get_event_loop().time() - start
        msg = data.get("message", {}) or {}
        raw = (msg.get("content") or "").strip()
        thinking, final = _parse_think_blocks(raw)

        return {
            "content": final,
            "thinking": thinking,
            "raw": raw,
            "model": self.model,
            "time": round(elapsed, 2),
            "tokens": data.get("eval_count", 0) + data.get("prompt_eval_count", 0),
        }


# Global instance used by the bot
qwen3 = Qwen3Client()
