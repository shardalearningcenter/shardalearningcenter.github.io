---
layout: home
title: Home
---

<section class="hero">
  <div class="hero-inner reveal">
    <p class="hero-brand">Sharda<em>Learning</em>Center</p>
    <h1>Learn programming &amp; AI by building real projects</h1>
    <p>Practical courses from engineers who’ve shipped at scale. No fluff — code, ship, and grow.</p>
    <div class="cta-row">
      <a class="btn btn-primary" href="{{ '/courses/' | relative_url }}">Browse courses</a>
      <a class="btn btn-ghost" href="https://youtube.com/@ShardaLearningCenter" target="_blank" rel="noopener">Watch on YouTube</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="section-head">
    <h2>Why learn with us</h2>
    <p>Industry experience, project-first lessons, and a path from beginner to job-ready.</p>
  </div>
  <div class="card-grid">
    <div class="card">
      <h3>Real industry experience</h3>
      <p>Insights from Big Tech so you learn how software is actually built — not only textbook theory.</p>
    </div>
    <div class="card">
      <h3>AI &amp; coding made clear</h3>
      <p>From Python to LLMs, we break complex topics into practical, beginner-friendly steps.</p>
    </div>
    <div class="card">
      <h3>Students &amp; career switchers</h3>
      <p>Whether you’re starting out or changing careers, build a portfolio that proves you can ship.</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="section-head">
    <h2>Popular courses</h2>
    <p>Pick a track and start building today.</p>
  </div>
  <div class="card-grid">
    <div class="card">
      <div class="card-meta">Beginner</div>
      <h3><a href="{{ '/learn-python-ten-days/' | relative_url }}">Python in 10 days</a></h3>
      <p>Hands-on Python with challenges and real projects.</p>
    </div>
    <div class="card">
      <div class="card-meta">30 tutorials</div>
      <h3><a href="{{ '/ml-learning-roadmap/' | relative_url }}">ML Learning Roadmap</a></h3>
      <p>Case-study scikit-learn curriculum with exercises.</p>
    </div>
    <div class="card">
      <div class="card-meta">Advanced</div>
      <h3><a href="{{ '/llm-bootcamp/' | relative_url }}">LLM Bootcamp</a></h3>
      <p>Transformers, prompting, fine-tuning, and RAG projects.</p>
    </div>
    <div class="card">
      <div class="card-meta">Backend</div>
      <h3><a href="{{ '/golang-bootcamp/' | relative_url }}">Golang Bootcamp</a></h3>
      <p>Practical Go for backend services and APIs.</p>
    </div>
    <div class="card">
      <div class="card-meta">Interview</div>
      <h3><a href="{{ '/dsa-cheatsheet/' | relative_url }}">DSA cheatsheet</a></h3>
      <p>Patterns and must-know structures for tech interviews.</p>
    </div>
    <div class="card">
      <div class="card-meta">Systems</div>
      <h3><a href="{{ '/low-level-design/' | relative_url }}">Low-level design</a></h3>
      <p>Design clean, interview-ready object-oriented systems.</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="section-head">
    <h2>From the blog</h2>
    <p>Latest notes on AI, coding, and career skills.</p>
  </div>
  <div class="card-grid">
    {% for post in site.posts limit:6 %}
    <article class="card">
      <div class="card-meta">{{ post.date | date: "%b %-d, %Y" }}</div>
      <h3><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h3>
      <p>{{ post.excerpt | strip_html | truncate: 140 }}</p>
    </article>
    {% endfor %}
  </div>
  <p style="text-align:center;margin-top:1.75rem;">
    <a class="btn btn-secondary" href="{{ '/blog/' | relative_url }}">View all posts</a>
  </p>
</section>
