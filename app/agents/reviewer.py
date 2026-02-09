from __future__ import annotations

from app.services.llm import llm_service
from app.services.prompt_loader import load_prompt


async def review_draft(keyword: str, draft: str) -> tuple[str, str]:
    system_prompt = load_prompt("reviewer_system.txt")
    user_prompt = load_prompt("reviewer_user.txt", keyword=keyword, draft=draft)
    result = await llm_service.generate(system_prompt, user_prompt)

    # Parse response into reviewed content and feedback
    if "[피드백]" in result:
        parts = result.split("[피드백]", 1)
        reviewed = parts[0].replace("[수정된 글]", "").strip()
        feedback = parts[1].strip()
    else:
        reviewed = result
        feedback = "피드백이 별도로 제공되지 않았습니다."

    return reviewed, feedback
