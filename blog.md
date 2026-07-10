---
layout: default
title: Blog
permalink: /blog/
---

<section class="hero hero-compact">
  <div class="hero-inner">
    <p class="eyebrow">Updates</p>
    <h1>Blog</h1>
    <p>Practical notes on AI, programming, and building in public.</p>
  </div>
</section>

<section class="section">
  <div class="card-grid">
    {% for post in site.posts %}
    <article class="card">
      <div class="card-meta">{{ post.date | date: "%b %-d, %Y" }}</div>
      <h3><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h3>
      <p>{{ post.excerpt | strip_html | truncate: 160 }}</p>
      <p style="margin-top:0.85rem;"><a href="{{ post.url | relative_url }}">Read more →</a></p>
    </article>
    {% endfor %}
  </div>
</section>
