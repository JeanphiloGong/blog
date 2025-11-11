"""
业务模型,用于对文章对象做操作
"""
from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from typing import List, Optional

class PostStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"

@dataclass
class Post:
    author_id: int
    title: str
    content: str
    status: PostStatus = PostStatus.DRAFT
    tags: List[str] = field(default_factory=list)
    slug: str =""
    id: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    published_at: Optional[datetime] = None

    def publish(self, now: Optional[datetime] = None):
        """
        修改博客状态
        """
        if self.status == PostStatus.PUBLISHED:
            return
        self.status = PostStatus.PUBLISHED
        self.published_at = now or datetime.utcnow()
        self.updated_at = now or datetime.utcnow()

    def archive(self, now: Optional[datetime] = None):
        self.status = PostStatus.ARCHIVED
        self.updated_at = now or datetime.utcnow()

    def update_content(self, title: str, content: str, tags: List[str], slug: Optional[str] = None, now: Optional[datetime] = None):
        print(f"[domains]: 正在更新内容title: {title}, content: {content}")
        if title is not None:
            self.title = title
        if content is not None:
            self.content = content
        if tags is not None:
            self.tags = tags
        if slug is not None:
            self.slug = slug
        self.updated_at = now or datetime.utcnow()
