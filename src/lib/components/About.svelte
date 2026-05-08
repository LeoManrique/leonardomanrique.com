<script lang="ts">
	interface AboutData {
		title: string;
		subtitle: string;
		description: string;
		resume: string;
	}

	let { data }: { data: AboutData } = $props();
</script>

<section class="about section" id="about">
	<h2 class="section__title">{data.title}</h2>

	<div class="about__container container grid">
		<div class="about__data">
			<p class="about__description">{data.description}</p>

			<div class="about__buttons">
				{#if data.resume}
					<a
						href={data.resume}
						class="button button--flex"
						target="_blank"
						rel="noopener noreferrer"
					>
						See Full Resume<i class="uil uil-cloud-download button__icon"></i>
					</a>
				{/if}
			</div>
		</div>
	</div>
</section>
