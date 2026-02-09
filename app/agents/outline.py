from __future__ import annotations

from app.services.llm import llm_service
from app.services.prompt_loader import load_prompt


async def generate_outline(keyword: str, tone: str | None, language: str) -> str:
    system_prompt = load_prompt("outline_system.txt")
    user_prompt = load_prompt(
        "outline_user.txt",
        keyword=keyword,
        tone=tone or "",
        language=language,
    )
    return await llm_service.generate(system_prompt, user_prompt)
