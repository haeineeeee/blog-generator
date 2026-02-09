from __future__ import annotations

from app.services.llm import llm_service
from app.services.prompt_loader import load_prompt


async def generate_draft(keyword: str, outline: str, tone: str | None) -> str:
    system_prompt = load_prompt("writer_system.txt")
    user_prompt = load_prompt(
        "writer_user.txt",
        keyword=keyword,
        outline=outline,
        tone=tone or "",
    )
    return await llm_service.generate(system_prompt, user_prompt)
