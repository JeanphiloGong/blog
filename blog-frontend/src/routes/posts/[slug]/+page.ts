// src/routes/posts/[slug]/+page.ts
import type { PageLoad } from './$types';
import { getPostBySlug } from '$lib/api';
import type { PostResponse } from '$lib/types';

export const load: PageLoad = async ({ params }) => {
  const { slug } = params;
  const post: PostResponse = await getPostBySlug(slug);
  return { post };
};

