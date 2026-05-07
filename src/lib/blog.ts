import type { Component } from 'svelte';

export interface PostMetadata {
	title: string;
	date: string;
	readingTime: string;
	summary: string;
	tags?: string[];
}

export interface PostSummary extends PostMetadata {
	slug: string;
}

interface MdsvexModule {
	default: Component;
	metadata: PostMetadata;
}

const modules = import.meta.glob<MdsvexModule>('/src/content/blog/*/index.md', {
	eager: true
});

const slugFromPath = (path: string): string => {
	const match = path.match(/\/blog\/([^/]+)\/index\.md$/);
	if (!match) throw new Error(`Unexpected blog post path: ${path}`);
	return match[1];
};

const allPosts: Array<PostSummary & { component: Component }> = Object.entries(modules)
	.map(([path, mod]) => ({
		slug: slugFromPath(path),
		component: mod.default,
		...mod.metadata
	}))
	.sort((a, b) => b.date.localeCompare(a.date));

export const listPosts = (): PostSummary[] =>
	allPosts.map(({ component: _component, ...summary }) => summary);

export const getPost = (slug: string) => allPosts.find((p) => p.slug === slug);

export const allSlugs = (): string[] => allPosts.map((p) => p.slug);
