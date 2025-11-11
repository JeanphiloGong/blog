// src/lib/types.ts
export interface PostResponse {
  id: number;
  author_id: number;
  title: string;
  content: string;
  slug: string;
  status: string; // "draft" | "published" | "archived"
  tags: string[];
  created_at: string; // ISO 日期字符串
  updated_at: string;
  published_at: string | null;
}

export interface PostCreate {
  title: string;
  content: string;
  tags?: string[];
  author_id: number;
}

export interface PostUpdate {
  author_id: number;
  title?: string | null;
  content?: string | null;
  tags?: string[] | null;
}

export interface PostPublishRequest {
  author_id: number;
}

