from __future__ import annotations

from datetime import datetime
from pathlib import Path

from slugify import slugify

from app.config import settings


async def save_markdown(title: str, content: str, filename: str | None = None) -> str:
    output_dir = Path(settings.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if filename:
        safe_name = filename if filename.endswith(".md") else f"{filename}.md"
    else:
        date_str = datetime.now().strftime("%Y%m%d")
        slug = slugify(title, allow_unicode=True)
        safe_name = f"{date_str}_{slug}.md"

    file_path = output_dir / safe_name
    file_path.write_text(f"# {title}\n\n{content}", encoding="utf-8")

    return str(file_path)
