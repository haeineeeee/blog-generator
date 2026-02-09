import base64

import httpx
from fastapi import HTTPException

from app.config import settings


async def publish_to_wordpress(title: str, content: str, status: str = "draft") -> dict:
    if not settings.wordpress_url:
        raise HTTPException(status_code=400, detail="WordPress URL is not configured.")

    url = f"{settings.wordpress_url.rstrip('/')}/wp-json/wp/v2/posts"
    credentials = f"{settings.wordpress_username}:{settings.wordpress_app_password}"
    token = base64.b64encode(credentials.encode()).decode()

    headers = {
        "Authorization": f"Basic {token}",
        "Content-Type": "application/json",
    }
    payload = {
        "title": title,
        "content": content,
        "status": status,
    }

    async with httpx.AsyncClient(timeout=30) as client:
        try:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
        except httpx.TimeoutException:
            raise HTTPException(status_code=504, detail="WordPress API request timed out.")
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"WordPress API error: {e.response.text}",
            )

    data = response.json()
    return {
        "id": data.get("id"),
        "url": data.get("link", ""),
        "status": data.get("status", ""),
    }
