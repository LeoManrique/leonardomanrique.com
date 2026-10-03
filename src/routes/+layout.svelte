<script lang="ts">
	import Header from '#lib/components/Header.svelte';
	import '../styles.css';

	let { children } = $props();

	let showScrollUp = $state(false);

	function handleScroll() {
		const scrollTop = window.scrollY;

		// Header shadow on scroll
		const header = document.getElementById('header');
		if (header) {
			header.classList.toggle('scroll-header', scrollTop >= 80);
		}

		// Show scroll-up button
		showScrollUp = scrollTop >= 560;
	}

	function scrollToTop() {
		window.scrollTo({ top: 0, behavior: 'smooth' });
	}

	$effect(() => {
		window.addEventListener('scroll', handleScroll);
		return () => window.removeEventListener('scroll', handleScroll);
	});
</script>

<Header />

<main class="main">
	{@render children()}
</main>

<button
	class="scrollup"
	class:show-scroll={showScrollUp}
	id="scroll-up"
	onclick={scrollToTop}
	aria-label="Scroll to top"
>
	<i class="uil uil-arrow-up scrollup__icon"></i>
</button>
