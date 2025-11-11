# routers/posts.py
import logging
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query
from pydantic import BaseModel

from routers.schemas.posts import PostCreate, PostPublishRequest, PostResponse, PostUpdate
from routers.dependencies import get_blog_service
from services.blog_service import BlogService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/posts", response_model=List[PostResponse])
def list_published_posts(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    tag: Optional[str] = None,
    author_id: Optional[int] = None,
    service: BlogService = Depends(get_blog_service),
):
    posts = service.list_published_posts(
        limit=limit,
        offset=offset,
        tag=tag,
        author_id=author_id,
    )
    # 直接返回领域模型，让 Pydantic 做转换
    return [
        PostResponse(
            id=p.id,
            author_id=p.author_id,
            title=p.title,
            content=p.content,
            slug=p.slug,
            status=p.status.value,
            tags=p.tags,
            created_at=p.created_at,
            updated_at=p.updated_at,
            published_at=p.published_at,
        )
        for p in posts
    ]

@router.get("/posts/{slug}", response_model=PostResponse)
def get_post_by_slug(
    slug: str,
    service: BlogService = Depends(get_blog_service),
):
    """
    通过构建的slug获取文章
    """
    post = service.get_post_by_slug_for_reader(slug)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return PostResponse(
        id=post.id,
        author_id=post.author_id,
        title=post.title,
        content=post.content,
        slug=post.slug,
        status=post.status.value,
        tags=post.tags,
        created_at=post.created_at,
        updated_at=post.updated_at,
        published_at=post.published_at,
    )

@router.post("/posts", response_model=PostResponse)
def create_post(
    payload: PostCreate,
    service: BlogService = Depends(get_blog_service),
):
    post = service.create_draft(
        author_id=payload.author_id,
        title=payload.title,
        content=payload.content,
        tags=payload.tags,
    )
    return PostResponse(
        id=post.id,
        author_id=post.author_id,
        title=post.title,
        content=post.content,
        slug=post.slug,
        status=post.status.value,
        tags=post.tags,
        created_at=post.created_at,
        updated_at=post.updated_at,
        published_at=post.published_at,
    )

def parse_tags_str(tags_str: str | None):
    if not tags_str:
        return []
    return [t.strip() for t in tags_str.split(",") if t.strip()]


@router.post("/posts/upload-markdown", response_model=PostResponse)
async def upload_markdown_post(
    file: UploadFile = File(...),
    author_id: int = Form(...),
    default_title: str = Form("Untitled"),
    default_tags: str = Form(""),
    service: BlogService = Depends(get_blog_service),
):
    if not file.filename.endswith(".md"):
        raise HTTPException(status_code=400, detail="Only .md files are allowed.")

    content_bytes = await file.read()
    markdown_content = content_bytes.decode("utf-8")

    post = service.create_from_markdown(
        author_id=author_id,
        markdown_content=markdown_content,
        default_title=default_title,
        default_tags=parse_tags_str(default_tags),
    )

    return PostResponse(
        id=post.id,
        author_id=post.author_id,
        title=post.title,
        content=post.content,
        slug=post.slug,
        status=post.status.value,
        tags=post.tags,
        created_at=post.created_at,
        updated_at=post.updated_at,
        published_at=post.published_at,
    )

@router.put("/posts/{post_id}", response_model=PostResponse)
def update_post(
    post_id: int,
    payload: PostUpdate,
    service: BlogService = Depends(get_blog_service),
):
    try:
        post = service.update_post(
            post_id=post_id,
            author_id=payload.author_id,
            title=payload.title,
            content=payload.content,
            tags=payload.tags,
        )
    except PermissionError:
        raise HTTPException(status_code=403, detail="Not allowed")
    except ValueError:
        raise HTTPException(status_code=404, detail="Post not found")

    return PostResponse(
        id=post.id,
        author_id=post.author_id,
        title=post.title,
        content=post.content,
        slug=post.slug,
        status=post.status.value,
        tags=post.tags,
        created_at=post.created_at,
        updated_at=post.updated_at,
        published_at=post.published_at,
    )


@router.post("/posts/{post_id}/publish", response_model=PostResponse)
def publish_post(
    post_id: int,
    payload: PostPublishRequest,
    service: BlogService = Depends(get_blog_service),
):
    try:
        logger.info(f"用户 {payload.author_id} 正在发布post {post_id} ")
        post = service.publish_post(
            post_id=post_id,
            author_id=payload.author_id,
        )
    except PermissionError:
        raise HTTPException(status_code=403, detail="Not allowed")
    except ValueError:
        raise HTTPException(status_code=404, detail="Post not found")

    return PostResponse(
        id=post.id,
        author_id=post.author_id,
        title=post.title,
        content=post.content,
        slug=post.slug,
        status=post.status.value,
        tags=post.tags,
        created_at=post.created_at,
        updated_at=post.updated_at,
        published_at=post.published_at,
    )


