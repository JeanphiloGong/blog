import logging
from datetime import datetime
from typing import List, Optional
from domains.posts import Post, PostStatus
from infra.posts import BasePostRepo

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BlogService:
    """
    博客应用服务层
    """
    def __init__(self, repo: BasePostRepo):
        self.repo = repo

    def create_draft(
            self,
            *,
            author_id: int,
            title: str,
            content: str,
            tags: Optional[List[str]] = None,
            ) -> Post:
        """
        创建一篇草稿
        """
        tags = tags or []
        slug = self._generate_slug(title)
        post = Post(
                author_id=author_id,
                title=title,
                content=content,
                slug=slug,
                tags=tags,
                status=PostStatus.DRAFT
                )
        return self.repo.save(post)

    def update_post(
            self,
            *,
            post_id: int,
            author_id: int,
            title: Optional[str] = None,
            content: Optional[str] = None,
            tags: Optional[List[str]] = None,
            ) -> Post:
        """
        更新文章
        """
        post = self.repo.get_post_by_id(post_id)
        print(f"[services]正在更新文章, {post}")
        if post is None:
            raise ValueError("Post not found")
        if post.author_id != author_id:
            raise PermissionError("You are not the author of the post")

        new_slug = None
        if title is not None and title != post.title:
            new_slug = self._generate_slug(title)

        print(f"传入参数为title: {title}, content: {content}")
        post.update_content(
                title=title,
                content=content,
                tags=tags,
                slug=new_slug,
                )

        return self.repo.save(post)

    def publish_post(self, *, post_id:int, author_id: int) -> Post:
        post = self.repo.get_post_by_id(post_id)
        if post is None:
            logger.info(f"Post {post_id} not found")
            raise ValueError("Post not Found")
        post.publish()
        return self.repo.save(post)

    def list_published_posts(
            self,
            *,
            limit: int = 10,
            offset: int = 0,
            tag: Optional[str] = None,
            author_id: Optional[int] = None,
            published_before: Optional[datetime] = None,
            ):
        print(f"[service]: 正在查询列表")
        result = self.repo.list_published(
                limit=limit,
                offset=offset,
                tag=tag,
                author_id=author_id,
                published_before=published_before,
                )
        print(f"[service] Result : {result}")
        return result

    def get_post_by_slug_for_reader(self, slug: str) -> Optional[Post]:
        post = self.repo.get_post_by_slug(slug)
        if post is None:
            print("该post为空")
            return None
        if post.status != PostStatus.PUBLISHED:
            print(f"该post未发布")
            return None
        print(f"查询结果为: {post}")
        return post

    def create_from_markdown(
            self,
            *,
            author_id: int,
            markdown_content: str,
            default_title: str = "Untitled",
            default_tags: Optional[List[str]] = None,
            ) -> Post:
        """
        从markdown内容创建文章:
         - content先保存完整markdown
         - title/tags 使用解析
         - 如果解析失败就使用default_title / default_tags
        """
        default_tags = default_tags or []


        # 2.使用parsing从markdown中解析元信息
        title, tags = self._parsing_md(markdown_content)
        if not title:
            title = default_title
        if not tags:
            tags = default_tags

        slug = self._generate_slug(title)

        post = Post(
                author_id=author_id,
                title=title,
                content=markdown_content,
                slug=slug,
                tags=tags,
                status=PostStatus.DRAFT,
                )

        return self.repo.save(post)

    def _parsing_md(self, markdown_content: str) -> tuple[Optional[str], Optional[List[str]]]:
        """
        解析markdown中的title/tags:
        """
        return None, None


    def _generate_slug(self, title: str) -> str:
        base = "-".join(title.strip().lower().split())
        if not base:
            base = "post"
        slug = base
        index = 1

        while self.repo.get_post_by_slug(slug) is not None:
            slug = f"{base}-{index}"
            index += 1
        return slug

