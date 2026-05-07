<script lang="ts">
	let { data } = $props();
	const Post = $derived(data.component);
	const metadata = $derived(data.metadata);

	const dateFormatter = new Intl.DateTimeFormat('en-US', {
		year: 'numeric',
		month: 'short',
		day: 'numeric'
	});
</script>

<svelte:head>
	<title>{metadata.title} — Leonardo Manrique</title>
	<meta name="description" content={metadata.summary} />
	<meta property="og:title" content={metadata.title} />
	<meta property="og:description" content={metadata.summary} />
	<meta property="og:type" content="article" />
</svelte:head>

<section class="post section">
	<div class="post__container container">
		<a href="/blog" class="post__back">
			<i class="uil uil-arrow-left"></i> Back to blog
		</a>

		<header class="post__header">
			<h1 class="post__title">{metadata.title}</h1>
			<div class="post__meta">
				<time datetime={metadata.date}>{dateFormatter.format(new Date(metadata.date))}</time>
				<span class="post__dot">·</span>
				<span>{metadata.readingTime}</span>
			</div>

			{#if metadata.tags?.length}
				<ul class="post__tags">
					{#each metadata.tags as tag}
						<li class="post__tag">{tag}</li>
					{/each}
				</ul>
			{/if}
		</header>

		<article class="post__body">
			<Post />
		</article>
	</div>
</section>
