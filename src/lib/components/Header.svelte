<script lang="ts">
	import { page } from '$app/state';
	import ThemeToggle from './ThemeToggle.svelte';

	const navLinks = [
		{ href: '/', label: 'Home' },
		{ href: '/portfolio/', label: 'Portfolio' },
		{ href: '/blog/', label: 'Blog' }
	];
</script>

<header class="header" id="header">
	<nav class="nav container">
		<a href="/" class="nav__logo">Leonardo</a>

		<div class="nav__menu">
			<ul class="nav__list">
				{#each navLinks as link}
					<li class="nav__item">
						<a
							href={link.href}
							class="nav__link"
							class:active-link={page.url.pathname === link.href}
						>
							{link.label}
						</a>
					</li>
				{/each}
			</ul>
		</div>

		<ThemeToggle />
	</nav>
</header>

<style>
	.nav__menu {
		display: flex;
		align-items: center;
	}

	.nav__list {
		display: flex;
		column-gap: 2rem;
		list-style: none;
		margin: 0;
		padding: 0;
	}

	.nav__link {
		color: var(--title-color);
		font-weight: var(--font-medium);
		transition: color 0.3s;
	}

	.nav__link:hover,
	.nav__link.active-link {
		color: var(--first-color);
	}
</style>
