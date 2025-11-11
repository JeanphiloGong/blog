<script lang="ts">
  import { onMount } from 'svelte';
  import { updatePost, publishPost } from '$lib/api';
  import type { PostResponse } from '$lib/types';

  export let params: { id: string };

  let postId = Number(params.id);
  let authorId = 0; // 实际上应该根据登录用户填，这里先手动
  let title = '';
  let content = '';
  let tags = '';
  let message: string | null = null;
  let error: string | null = null;

  // 可选：如果你有按 ID 获取文章的接口，可以在这里加载现有内容
  // onMount(async () => { ... });

  async function handleUpdate() {
    error = null;
    message = null;

    try {
      const res = await updatePost(postId, {
        author_id: authorId,
        title,
        content,
        tags: tags
          ? tags.split(',').map((t) => t.trim()).filter(Boolean)
          : []
      });
      message = `更新成功，slug=${res.slug}`;
    } catch (e: any) {
      error = e.message ?? String(e);
    }
  }

  async function handlePublish() {
    error = null;
    message = null;

    try {
      const res: PostResponse = await publishPost(postId, { author_id: authorId });
      message = `发布成功，状态=${res.status}, 发布时间=${res.published_at}`;
    } catch (e: any) {
      error = e.message ?? String(e);
    }
  }
</script>

<svelte:head>
  <title>编辑文章 #{postId} - 管理后台</title>
</svelte:head>

<main class="container">
  <a href="/">← 返回列表</a>
  <h1>编辑文章 #{postId}</h1>

  {#if error}
    <p class="error">{error}</p>
  {/if}
  {#if message}
    <p class="success">{message}</p>
  {/if}

  <form on:submit|preventDefault={handleUpdate}>
    <label>
      作者 ID
      <input type="number" bind:value={authorId} min="0" />
    </label>

    <label>
      标题
      <input type="text" bind:value={title} />
    </label>

    <label>
      标签（逗号分隔）
      <input type="text" bind:value={tags} />
    </label>

    <label>
      内容
      <textarea bind:value={content} rows="10" />
    </label>

    <button type="submit">保存修改</button>
  </form>

  <button class="publish-btn" on:click|preventDefault={handlePublish}>
    发布文章
  </button>
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
    margin-bottom: 1rem;
  }
  .error {
    color: #b91c1c;
  }
  .success {
    color: #15803d;
  }
  .publish-btn {
    padding: 0.4rem 0.8rem;
    border-radius: 4px;
    border: none;
    background: #16a34a;
    color: white;
    cursor: pointer;
  }
</style>

