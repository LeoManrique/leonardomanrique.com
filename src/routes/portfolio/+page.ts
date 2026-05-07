import type { PageLoad } from './$types';

export const load: PageLoad = async ({ fetch }) => {
	const res = await fetch('/assets/data/portfolio.json');
	return await res.json();
};
