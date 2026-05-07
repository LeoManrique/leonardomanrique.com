import type { PageLoad } from './$types';
import { listPosts } from '$lib/blog';

export const load: PageLoad = () => {
	return { posts: listPosts() };
};
