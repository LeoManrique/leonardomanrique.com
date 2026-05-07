<script lang="ts">
	import type { PostSummary } from '$lib/blog';

	let { data }: { data: { posts: PostSummary[] } } = $props();

	const dateFormatter = new Intl.DateTimeFormat('en-US', {
		year: 'numeric',
		month: 'short',
		day: 'numeric'
	});
</script>

<svelte:head>
	<title>Blog — Leonardo Manrique</title>
	<meta name="description" content="Thoughts and learnings from Leonardo Manrique on software development." />
	<meta property="og:title" content="Blog — Leonardo Manrique" />
	<meta property="og:description" content="Thoughts and learnings from Leonardo Manrique on software development." />
	<meta property="og:url" content="https://www.leonardomanrique.com/blog" />
</svelte:head>

<section class="blog section" id="blog">
	<h2 class="section__title">Blog</h2>
	<span class="section__subtitle">Thoughts and learnings</span>

	<div class="blog__container container">
		{#each data.posts as post}
			<article class="blog__card">
				<header class="blog__meta">
					<time datetime={post.date}>{dateFormatter.format(new Date(post.date))}</time>
					<span class="blog__dot">·</span>
					<span>{post.readingTime}</span>
				</header>

				<h3 class="blog__title">
					<a href="/blog/{post.slug}">{post.title}</a>
				</h3>

				<p class="blog__summary">{post.summary}</p>

				{#if post.tags?.length}
					<ul class="blog__tags">
						{#each post.tags as tag}
							<li class="blog__tag">{tag}</li>
						{/each}
					</ul>
				{/if}

				<a href="/blog/{post.slug}" class="blog__link">
					Read more <i class="uil uil-arrow-right"></i>
				</a>
			</article>
		{/each}
	</div>
</section>
