<script lang="ts">
  import { uploadMarkdownPost } from '$lib/api';
  import type { PostResponse } from '$lib/types';

  let file: File | null = null;
  let authorId = 0;
  let defaultTitle = '';
  let defaultTags = '';
  let error: string | null = null;
  let success: string | null = null;
  let lastPost: PostResponse | null = null;  // ⭐ 保存上传成功后的文章

  function handleFileChange(event: Event) {
    const input = event.currentTarget as HTMLInputElement;
    file = input.files?.[0] ?? null;
  }

  async function handleSubmit() {
    error = null;
    success = null;
    lastPost = null;

    if (!file) {
      error = '请先选择一个 Markdown 文件';
      return;
    }

    try {
      const res = await uploadMarkdownPost(
        file,
        authorId,
        defaultTitle || file.name.replace(/\.md$/i, ''),
        defaultTags
      );
      lastPost = res;  // ⭐ 保存起来
      success = `上传成功：ID=${res.id}, slug=${res.slug}`;
    } catch (e: any) {
      error = e.message ?? String(e);
    }
  }
</script>

<main class="container">
  <a href="/">← 返回列表</a>
  <h1>上传 Markdown 文件</h1>

  {#if error}
    <p class="error">{error}</p>
  {/if}
  {#if success}
    <p class="success">{success}</p>

    {#if lastPost}
      <div class="actions">
        <!-- 查看前台文章（目前还是 draft，但可以调试） -->
        <a class="btn" href={`/posts/${lastPost.slug}`} target="_blank">
          查看文章详情
        </a>

        <!-- 去编辑 / 发布页面 -->
        <a class="btn primary" href={`/admin/posts/${lastPost.id}/edit`}>
          去编辑 / 发布
        </a>
      </div>
    {/if}
  {/if}

  <form on:submit|preventDefault={handleSubmit}>
    <label>
      作者 ID
      <input type="number" bind:value={authorId} min="0" />
    </label>

    <label>
      Markdown 文件
      <input type="file" accept=".md,text/markdown" on:change={handleFileChange} />
    </label>

    <label>
      默认标题（可选，不填时使用文件名）
      <input type="text" bind:value={defaultTitle} />
    </label>

    <label>
      默认标签（可选，逗号分隔）
      <input type="text" bind:value={defaultTags} />
    </label>

    <button type="submit">上传</button>
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
  .error {
    color: #b91c1c;
  }
  .success {
    color: #15803d;
  }
  .actions {
    margin: 0.5rem 0 1rem;
    display: flex;
    gap: 0.5rem;
  }
  .btn {
    display: inline-block;
    padding: 0.3rem 0.8rem;
    border-radius: 4px;
    text-decoration: none;
    background: #6b7280;
    color: white;
    font-size: 0.9rem;
  }
  .btn.primary {
    background: #2563eb;
  }
</style>

