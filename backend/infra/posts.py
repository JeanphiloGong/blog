from typing import Dict, Protocol, List, Optional
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import (
    Integer,
    String,
    Text,
    DateTime,
    select,
    func
)

from infra.db import get_db, Base
from domains.posts import PostStatus, Post

########################################
#  ORM 模型
###########################################

class PostORM(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    author_id: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="draft")
    tags: Mapped[str] = mapped_column(String(255), default="")  # 简单做成逗号分隔的字符串

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    published_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    def __repr__(self) -> str:
        return f"<PostORM id={self.id} title={self.title!r}>"


#######################################
#  操作方法
###################################
class BasePostRepo(Protocol):
    def save(self, post: Post) -> Post:
        """
        保存 新建文章
        """
    def get_post_by_id(self, post_id: int) -> Optional[Post]:
        ...

    def get_post_by_slug(self, slug: str) -> Optional[Post]:
        ...

    def list_published(
            self,
            *,
            limit: int=10,
            offset: int = 0,
            tag: Optional[str] = None,
            author_id: Optional[int] = None,
            published_before: Optional[datetime] = None,
            ) -> List[Post]:
        ...

class testPostRepo(BasePostRepo):
    def __init__(self):
        self._posts: Dict[int, Post] = {}
        self._next_id: int = 1

    def next_id(self) -> int:
        nid = self._next_id
        self._next_id += 1
        return nid

    def save(self, post: Post) -> Post:
        if post.id is None:
            post.id = self.next_id()
        self._posts[post.id] = post
        return post

    def get_post_by_id(self, post_id: int) -> Optional[Post]:
        return self._posts.get(post_id)

    def get_post_by_slug(self, slug: str) -> Optional[Post]:
        print(f"[repo] 正在通过slug: {slug} 查询记录")
        for post in self._posts.values():
            print(f"post.sulg: {post.slug}, slug: {slug}")
            if post.slug == slug:
                print("查询成功")
                return post
        print("查询失败")
        return None

    def list_published(self, *, limit: int = 10, offset: int = 0, tag: Optional[str] = None, author_id: Optional[int] = None, published_before: Optional[datetime] = None) -> List[Post]:
        posts = [
                p for p in self._posts.values() if p.status == PostStatus.PUBLISHED
                 ]
        print(f"[repo] 查询到列表为 {posts}")

        if tag is not None:
            posts = [p for p in posts if tag in p.tags]

        if author_id is not None:
            posts = [p for p in posts if p.author_id == author_id]

        if published_before is not None:
            posts = [
                    p for p in posts
                    if p.published_at and p.published_at <= published_before
                    ]

        posts.sort(
                key=lambda p: p.published_at or p.created_at,
                reverse=True,
                )
        print(f"[repo] 筛选后的列表为 {posts}, Result: {posts[offset:offset+limit]}")

        return posts[offset:offset+limit]


class PostRepo(BasePostRepo):
    """
    使用sqlalchemy
    """
    def save(self, post: Post) -> Post:
        with get_db() as db:
            if post.id is not None:
                orm = db.get(PostORM, post.id)
            else:
                orm = None

            orm = domain_to_orm(post, orm)
            db.add(orm)
            db.commit()
            db.refresh(orm)

            post.id = orm.id
            return orm_to_domain(orm)

    def get_post_by_slug(self, slug: str) -> Optional[Post]:
        with get_db() as db:
            stmt = select(PostORM).where(PostORM.slug == slug)
            orm = db.execute(stmt).scalar_one_or_none()
            if orm is None:
                return None
            return orm_to_domain(orm)

    def get_post_by_id(self, post_id: int) -> Optional[Post]:
        with get_db() as db:
            orm = db.get(PostORM, post_id)
            if orm is None:
                return None
            return orm_to_domain(orm)

    def list_published(self, *, limit: int = 10, offset: int = 0, tag: Optional[str] = None, author_id: Optional[int] = None, published_before: Optional[datetime] = None) -> List[Post]:
        with get_db() as db:
            stmt = select(PostORM).where(PostORM.status == PostStatus.PUBLISHED.value)

            if tag is not None:
                stmt = stmt.where(PostORM.tags.like(f"%{tag}%"))
            if author_id is not None:
                stmt = stmt.where(PostORM.author_id == author_id)

            if published_before is not None:
                stmt = stmt.where(PostORM.published_at <= published_before)

            stmt = stmt.order_by(
                    PostORM.published_at.desc().nullslast(),
                    PostORM.created_at.desc(),
                    ).offset(offset).limit(limit)

            result = db.execute(stmt).scalars().all()
            return [orm_to_domain(orm) for orm in result]

#####################################
# 操作方法
#################################
def _tags_str_to_list(tags_str: str) -> List[str]:
    if not tags_str:
        return []
    return [t.strip() for t in tags_str.split(",") if t.strip()]


def _tags_list_to_str(tags: List[str]) -> str:
    return ",".join(tags)

def orm_to_domain(orm: PostORM) -> Post:
    return Post(
        id=orm.id,
        author_id=orm.author_id,
        title=orm.title,
        content=orm.content,
        slug=orm.slug,
        status=PostStatus(orm.status),
        tags=_tags_str_to_list(orm.tags),
        created_at=orm.created_at,
        updated_at=orm.updated_at,
        published_at=orm.published_at,
    )


def domain_to_orm(post: Post, orm: Optional[PostORM] = None) -> PostORM:
    """
    如果 orm 为 None，则创建新的 PostORM；
    否则在已有 orm 对象上更新字段。
    """
    if orm is None:
        orm = PostORM()
    orm.author_id = post.author_id
    orm.title = post.title
    orm.content = post.content
    orm.slug = post.slug
    orm.status = post.status.value
    orm.tags = _tags_list_to_str(post.tags)
    orm.created_at = post.created_at
    orm.updated_at = post.updated_at
    orm.published_at = post.published_at

    return orm

