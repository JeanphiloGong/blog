<script lang="ts">
  import type { PageData } from './$types';

  export let data: PageData;
  const { post } = data;
</script>

<svelte:head>
  <title>{post.title} - 博客</title>
</svelte:head>

<main class="container">
  <a href="/">← 返回列表</a>
  <article>
    <h1>{post.title}</h1>
    <p class="meta">
      <span>作者 ID: {post.author_id}</span>
      {#if post.published_at}
        <span>发布时间: {new Date(post.published_at).toLocaleString()}</span>
      {/if}
    </p>

    {#if post.tags.length}
      <p class="tags">
        {#each post.tags as tag}
          <span class="tag">{tag}</span>
        {/each}
      </p>
    {/if}

    <pre class="content">{post.content}</pre>
    <!-- 这里 content 目前是 Markdown 原文，你以后可以用 markdown 渲染 -->
  </article>
</main>

<style>
  .container {
    max-width: 800px;
    margin: 2rem auto;
    padding: 0 1rem;
  }
  .meta {
    font-size: 0.85rem;
    color: #666;
    display: flex;
    gap: 1rem;
  }
  .tag {
    display: inline-block;
    background: #f0f0f0;
    padding: 0.1rem 0.4rem;
    margin-right: 0.3rem;
    border-radius: 4px;
    font-size: 0.8rem;
  }
  .content {
    white-space: pre-wrap;
    line-height: 1.6;
    margin-top: 1rem;
  }
</style>

