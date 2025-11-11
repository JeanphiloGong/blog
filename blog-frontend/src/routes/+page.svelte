<script lang="ts">
  import type { PageData } from './$types';

  export let data: PageData;
  const { posts } = data;
</script>

<svelte:head>
  <title>博客 - 首页</title>
</svelte:head>

<main class="container">
  <h1>博客文章</h1>

  {#if posts.length === 0}
    <p>目前还没有文章。</p>
  {:else}
    <ul class="post-list">
      {#each posts as post}
        <li>
          <a href={`/posts/${post.slug}`}>
            <h2>{post.title}</h2>
          </a>
          <p class="meta">
            <span>作者 ID: {post.author_id}</span>
            <span>创建时间: {new Date(post.created_at).toLocaleString()}</span>
          </p>
          {#if post.tags.length}
            <p class="tags">
              {#each post.tags as tag}
                <span class="tag">{tag}</span>
              {/each}
            </p>
          {/if}
        </li>
      {/each}
    </ul>
  {/if}

  <a class="btn" href="/admin/posts/new">写新文章</a>
  <a class="btn secondary" href="/admin/posts/md-upload">上传 Markdown</a>
</main>

<style>
  .container {
    max-width: 800px;
    margin: 2rem auto;
    padding: 0 1rem;
  }
  .post-list {
    list-style: none;
    padding: 0;
  }
  .post-list li {
    border-bottom: 1px solid #eee;
    padding: 1rem 0;
  }
  .meta {
    font-size: 0.85rem;
    color: #666;
    display: flex;
    gap: 1rem;
  }
  .tags {
    margin-top: 0.5rem;
  }
  .tag {
    display: inline-block;
    background: #f0f0f0;
    padding: 0.1rem 0.4rem;
    margin-right: 0.3rem;
    border-radius: 4px;
    font-size: 0.8rem;
  }
  .btn {
    display: inline-block;
    margin-top: 1rem;
    margin-right: 0.5rem;
    padding: 0.4rem 0.8rem;
    border-radius: 4px;
    background: #2563eb;
    color: white;
    text-decoration: none;
  }
  .btn.secondary {
    background: #6b7280;
  }
</style>

