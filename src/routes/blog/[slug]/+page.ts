import type { EntryGenerator, PageLoad } from './$types';
import { error } from '@sveltejs/kit';
import { allSlugs, getPost } from '$lib/blog';

export const prerender = true;

export const entries: EntryGenerator = () => allSlugs().map((slug) => ({ slug }));

export const load: PageLoad = ({ params }) => {
	const post = getPost(params.slug);
	if (!post) throw error(404, 'Post not found');

	const { component, ...metadata } = post;
	return { component, metadata };
};
