// src/lib/api.ts
import type {
  PostCreate,
  PostResponse,
  PostUpdate,
  PostPublishRequest
} from './types';

const BASE_URL = 'http://localhost:8000';

async function api<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: {
      'Content-Type': init?.body instanceof FormData ? undefined : 'application/json',
      ...(init?.headers || {})
    },
    ...init
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`API error ${res.status}: ${text}`);
  }
  return res.json() as Promise<T>;
}

// 列出已发布文章
export async function listPublishedPosts(params?: {
  limit?: number;
  offset?: number;
  tag?: string;
  author_id?: number;
}): Promise<PostResponse[]> {
  const search = new URLSearchParams();
  if (params?.limit) search.set('limit', String(params.limit));
  if (params?.offset) search.set('offset', String(params.offset));
  if (params?.tag) search.set('tag', params.tag);
  if (params?.author_id != null) search.set('author_id', String(params.author_id));

  const query = search.toString();
  return api<PostResponse[]>(`/posts${query ? `?${query}` : ''}`);
}

// 根据 slug 获取文章
export async function getPostBySlug(slug: string): Promise<PostResponse> {
  return api<PostResponse>(`/posts/${encodeURIComponent(slug)}`);
}

// 创建草稿
export async function createPost(payload: PostCreate): Promise<PostResponse> {
  return api<PostResponse>('/posts', {
    method: 'POST',
    body: JSON.stringify(payload)
  });
}

// 更新文章
export async function updatePost(postId: number, payload: PostUpdate): Promise<PostResponse> {
  return api<PostResponse>(`/posts/${postId}`, {
    method: 'PUT',
    body: JSON.stringify(payload)
  });
}

// 发布文章
export async function publishPost(postId: number, payload: PostPublishRequest): Promise<PostResponse> {
  return api<PostResponse>(`/posts/${postId}/publish`, {
    method: 'POST',
    body: JSON.stringify(payload)
  });
}

// 上传 markdown 创建草稿
export async function uploadMarkdownPost(
  file: File,
  authorId: number,
  defaultTitle = 'Untitled',
  defaultTags = ''
): Promise<PostResponse> {
  const form = new FormData();
  form.append('file', file);
  form.append('author_id', String(authorId));
  form.append('default_title', defaultTitle);
  form.append('default_tags', defaultTags);

  const res = await fetch(`${BASE_URL}/posts/upload-markdown`, {
    method: 'POST',
    body: form
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`API error ${res.status}: ${text}`);
  }
  return res.json() as Promise<PostResponse>;
}

