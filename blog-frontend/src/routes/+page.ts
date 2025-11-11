// src/routes/+page.ts
import type { PageLoad } from './$types';
import { listPublishedPosts } from '$lib/api';
import type { PostResponse } from '$lib/types';

export const load: PageLoad = async () => {
  const posts: PostResponse[] = await listPublishedPosts({ limit: 20 });
  return { posts };
};

