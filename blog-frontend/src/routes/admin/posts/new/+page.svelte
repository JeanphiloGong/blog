<script lang="ts">
  import { createPost } from '$lib/api';
  import type { PostCreate } from '$lib/types';

  let title = '';
  let content = '';
  let tags = '';
  let authorId = 0;
  let error: string | null = null;
  let success: string | null = null;

  async function handleSubmit() {
    error = null;
    success = null;

    if (!title || !content) {
      error = '标题和内容不能为空';
      return;
    }

    const payload: PostCreate = {
      title,
      content,
      author_id: authorId,
      tags: tags
        ? tags.split(',').map((t) => t.trim()).filter(Boolean)
        : []
    };

    try {
      const post = await createPost(payload);
      success = `创建成功，ID=${post.id}, slug=${post.slug}`;
    } catch (e: any) {
      error = e.message ?? String(e);
    }
  }
</script>

<svelte:head>
  <title>新建文章 - 管理后台</title>
</svelte:head>

<main class="container">
  <a href="/">← 返回列表</a>
  <h1>新建文章</h1>

  {#if error}
    <p class="error">{error}</p>
  {/if}
  {#if success}
    <p class="success">{success}</p>
  {/if}

  <form on:submit|preventDefault={handleSubmit}>
    <label>
      作者 ID
      <input type="number" bind:value={authorId} min="0" />
    </label>

    <label>
      标题
      <input type="text" bind:value={title} />
    </label>

    <label>
      标签（用逗号分隔）
      <input type="text" bind:value={tags} placeholder="python, blog" />
    </label>

    <label>
      内容
      <textarea bind:value={content} rows="10" />
    </label>

    <button type="submit">创建草稿</button>
  </form>
</main>

<style>
  .container {
    max-width: 800px;
    margin: 2rem auto;
    padding: 0 1rem;
  }
  form {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
  label {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
  }
  input,
  textarea {
    padding: 0.4rem;
    border-radius: 4px;
    border: 1px solid #ccc;
  }
  .error {
    color: #b91c1c;
  }
  .success {
    color: #15803d;
  }
</style>

