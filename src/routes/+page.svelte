<script lang="ts">
	import Home from '$lib/components/Home.svelte';
	import About from '$lib/components/About.svelte';
	import Qualification from '$lib/components/Qualification.svelte';

	let { data } = $props();
</script>

<svelte:head>
	<title>Leonardo Manrique — Backend Engineer</title>
	<meta name="description" content="Leonardo Manrique — Backend Engineer specialized in integrations and extensions for enterprise systems." />
	<meta property="og:title" content="Leonardo Manrique — Backend Engineer" />
	<meta property="og:description" content="Backend Backend specialized in projects for enterprise systems." />
	<meta property="og:url" content="https://www.leonardomanrique.com/" />

	{@html `<script type="application/ld+json">${JSON.stringify({
		"@context": "https://schema.org",
		"@type": "ProfilePage",
		"mainEntity": {
			"@type": "Person",
			"name": "Leonardo Manrique",
			"jobTitle": "Backend Engineer",
			"description": "Backend Engineer specialized in projects for enterprise systems.",
			"url": "https://www.leonardomanrique.com",
			"image": "https://www.leonardomanrique.com/assets/img/profile.png",
			"sameAs": [
				"https://www.linkedin.com/in/leonardo-manrique-solano/",
				"https://github.com/LeoManrique",
				"https://www.instagram.com/leomanrique0502/"
			],
			"alumniOf": [
				{ "@type": "CollegeOrUniversity", "name": "Universidad San Ignacio de Loyola" },
				{ "@type": "CollegeOrUniversity", "name": "San Ignacio University" }
			],
			"worksFor": { "@type": "Organization", "name": "Avaloq" },
			"knowsAbout": ["Backend Development", "Oracle Database", "Java", "Enterprise Systems Integration"]
		}
	})}</script>`}
</svelte:head>

<Home data={data.home} />
<About data={data.about} />
<Qualification data={data.qualification} />
