from infra.posts import PostRepo
from services.blog_service import BlogService

_repo = PostRepo()
_service = BlogService(_repo)

def get_blog_service() -> BlogService:
    return _service
