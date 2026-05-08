import type { PageLoad } from './$types';
import portfolio from '$content/portfolio/portfolio.json';

export const load: PageLoad = () => portfolio;
