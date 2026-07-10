---
layout: default
title: Blog
permalink: /blog/
description: Practical notes on AI, programming, and building in public.
---

<nav class="docs-breadcrumb" aria-label="Breadcrumb">
  <a href="{{ '/' | relative_url }}">Home</a><span>/</span>
  <span class="docs-breadcrumb-current">Blog</span>
</nav>

<article class="docs-article docs-article-solo">
  <header class="docs-article-header">
    <p class="docs-eyebrow">Updates</p>
    <h1 class="docs-h1">Blog</h1>
    <p class="docs-lead">Practical notes on AI, programming, and building in public.</p>
  </header>
  <div class="docs-content">
    <div class="card-grid">
      {% for post in site.posts %}
      <article class="card">
        <div class="card-meta">{{ post.date | date: "%b %-d, %Y" }}</div>
        <h3><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h3>
        <p>{{ post.excerpt | strip_html | truncate: 160 }}</p>
      </article>
      {% endfor %}
    </div>
  </div>
</article>
