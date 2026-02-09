from anthropic import AsyncAnthropic, APIError, APITimeoutError, RateLimitError
from fastapi import HTTPException

from app.config import settings


class LLMService:
    def __init__(self):
        self.client = AsyncAnthropic(api_key=settings.anthropic_api_key)
        self.model = settings.claude_model

    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 4096,
        temperature: float = 0.7,
    ) -> str:
        try:
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}],
            )
            return response.content[0].text
        except RateLimitError:
            raise HTTPException(status_code=429, detail="Claude API rate limit exceeded. Please try again later.")
        except APITimeoutError:
            raise HTTPException(status_code=504, detail="Claude API request timed out.")
        except APIError as e:
            raise HTTPException(status_code=502, detail=f"Claude API error: {e.message}")


llm_service = LLMService()
