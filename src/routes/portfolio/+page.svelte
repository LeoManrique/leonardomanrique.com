<script lang="ts">
	interface Project {
		title: string;
		subtitle?: string;
		description: string;
		tags?: string[];
		url: string;
		icon?: string;
	}

	let { data }: { data: { projects: Project[] } } = $props();
</script>

<svelte:head>
	<title>Portfolio — Leonardo Manrique</title>
	<meta name="description" content="Projects and recent work by Leonardo Manrique." />
	<meta property="og:title" content="Portfolio — Leonardo Manrique" />
	<meta property="og:description" content="Projects and recent work by Leonardo Manrique." />
	<meta property="og:url" content="https://www.leonardomanrique.com/portfolio" />
</svelte:head>

<section class="portfolio section" id="portfolio">
	<h2 class="section__title">Portfolio</h2>
	<span class="section__subtitle">My recent work</span>

	<div class="portfolio__container container">
		{#each data.projects as project}
			<article class="portfolio__card">
				{#if project.icon}
					<div class="portfolio__icon-wrap">
						<i class="uil {project.icon} portfolio__icon"></i>
					</div>
				{/if}

				<div class="portfolio__body">
					<h3 class="portfolio__title">{project.title}</h3>
					{#if project.subtitle}
						<span class="portfolio__subtitle">{project.subtitle}</span>
					{/if}

					<p class="portfolio__description">{project.description}</p>

					{#if project.tags?.length}
						<ul class="portfolio__tags">
							{#each project.tags as tag}
								<li class="portfolio__tag">{tag}</li>
							{/each}
						</ul>
					{/if}

					<a
						href={project.url}
						class="button button--flex button--small portfolio__link"
						target="_blank"
						rel="noopener noreferrer"
					>
						View project <i class="uil uil-arrow-right button__icon"></i>
					</a>
				</div>
			</article>
		{/each}
	</div>
</section>
