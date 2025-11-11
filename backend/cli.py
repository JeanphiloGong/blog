# cli.py

import argparse
from typing import List
from pathlib import Path

from infra.posts import testPostRepo
from services.blog_service import BlogService

def parse_tags(tags_str: str | None) -> List[str]:
    if not tags_str:
        return []
    return [t.strip() for t in tags_str.split(",") if t.strip()]

def main():
    parser = argparse.ArgumentParser(description="Import a markdown file as a blog post.")
    parser.add_argument("--file", "-f", required=True,  help="Path to the markdown file.")
    parser.add_argument("--author-id", "-aid", type=int, required=True, help="Author ID.")
    parser.add_argument(
            "--default-title", 
            type=str, 
            default=None, 
            help="Default title if markdown parsing fails."
            )
    parser.add_argument(
            "--default-tags",
            type=str,
            default=None,
            help="comman-separated tags if markdown parsing fails",
            )

    args = parser.parse_args()

    # 1. Read markdown file
    with open(args.file, "r", encoding="utf-8") as f:
        markdown_content = f.read()

    file_stem = Path(args.file).stem
    effective_default_title = args.default_title or file_stem

    repo = testPostRepo()
    service = BlogService(repo)

    # 3.调用核心逻辑
    post = service.create_from_markdown(
            author_id=args.author_id,
            markdown_content=markdown_content,
            default_title=effective_default_title,
            default_tags=parse_tags(args.default_tags),
            )

    # 4. 打印结果
    print("Imported post:")
    print(f"  id: {post.id}")
    print(f"  title: {post.title}")
    print(f"  slug: {post.slug}")
    print(f"  status: {post.status}")
    print(f"  tags: {post.tags}")


if __name__ == "__main__":
    main()
