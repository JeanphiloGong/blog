from services.blog_service import BlogService
from infra.posts import testPostRepo

def main():
    repo = testPostRepo()
    service = BlogService(repo)

    draft = service.create_draft(
            author_id=1,
            title="测试博客",
            content="这是内容",
            tags=["python", "test"]
            )
    print("Draft created:", draft)

    draft = service.update_post(
            post_id = draft.id,
            author_id=1,
            content="更新后的内容"
            )
    print("Draft updated:", draft.content)

    published = service.publish_post(post_id=draft.id, author_id=1)
    print("Published:", published.status, published.published_at)

    posts = service.list_published_posts(limit=10)
    print(f"[demo] Posts: {posts}")
    print("Published posts", [p.title for p in posts])

    slug = published.slug
    print(f"[demo] 尝试通过slug {slug} 获取记录")
    post = service.get_post_by_slug_for_reader(slug)
    print("Get by slug", post.title if post else None)

if __name__ == "__main__":
    main()

