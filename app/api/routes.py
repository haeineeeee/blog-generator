from fastapi import APIRouter

from app.agents.outline import generate_outline
from app.agents.reviewer import review_draft
from app.agents.writer import generate_draft
from app.models.schemas import (
    DraftRequest,
    DraftResponse,
    FullGenerateRequest,
    FullGenerateResponse,
    MarkdownSaveRequest,
    OutlineRequest,
    OutlineResponse,
    PublishResponse,
    ReviewRequest,
    ReviewResponse,
    WordPressPublishRequest,
)
from app.services.markdown import save_markdown
from app.services.wordpress import publish_to_wordpress

router = APIRouter()


@router.post("/generate/outline", response_model=OutlineResponse)
async def outline_endpoint(req: OutlineRequest):
    outline = await generate_outline(req.keyword, req.tone, req.language)
    return OutlineResponse(keyword=req.keyword, outline=outline)


@router.post("/generate/draft", response_model=DraftResponse)
async def draft_endpoint(req: DraftRequest):
    draft = await generate_draft(req.keyword, req.outline, req.tone)
    return DraftResponse(keyword=req.keyword, outline=req.outline, draft=draft)


@router.post("/generate/review", response_model=ReviewResponse)
async def review_endpoint(req: ReviewRequest):
    reviewed, feedback = await review_draft(req.keyword, req.draft)
    return ReviewResponse(
        keyword=req.keyword,
        draft=req.draft,
        reviewed=reviewed,
        feedback=feedback,
    )


@router.post("/generate/full", response_model=FullGenerateResponse)
async def full_generate_endpoint(req: FullGenerateRequest):
    outline = await generate_outline(req.keyword, req.tone, req.language)
    draft = await generate_draft(req.keyword, outline, req.tone)
    reviewed, feedback = await review_draft(req.keyword, draft)
    return FullGenerateResponse(
        keyword=req.keyword,
        outline=outline,
        draft=draft,
        reviewed=reviewed,
        feedback=feedback,
    )


@router.post("/publish/wordpress", response_model=PublishResponse)
async def wordpress_endpoint(req: WordPressPublishRequest):
    result = await publish_to_wordpress(req.title, req.content, req.status)
    return PublishResponse(
        success=True,
        message="WordPress에 발행되었습니다.",
        url=result.get("url"),
    )


@router.post("/publish/markdown", response_model=PublishResponse)
async def markdown_endpoint(req: MarkdownSaveRequest):
    file_path = await save_markdown(req.title, req.content, req.filename)
    return PublishResponse(
        success=True,
        message=f"마크다운 파일이 저장되었습니다: {file_path}",
    )
