import type { PageLoad } from './$types';
import home from '$content/home/home.json';
import about from '$content/home/about.json';
import qualificationData from '$content/home/qualification.json';

interface QualificationItem {
	title: string;
	subtitle: string;
	date: string;
	position: 'left' | 'right';
}

const qualification = qualificationData as {
	work: QualificationItem[];
	education: QualificationItem[];
};

export const load: PageLoad = () => ({ home, about, qualification });
