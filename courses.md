---
layout: page
title: Courses
permalink: /courses/
---

<style>
  .body1 {
      margin: 0;
      font-family: 'Segoe UI', sans-serif;
      background: #f9f9f9;
      color: #333;
      scroll-behavior: smooth;
      width: 100%;
    }
.course-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}
.course-card {
  border: 1px solid #ccc;
  border-radius: 10px;
  padding: 1rem;
  background: var(--bg-card, #fff);
  box-shadow: 2px 2px 8px rgba(0,0,0,0.05);
  transition: transform 0.2s;
}
.course-card:hover {
  transform: translateY(-5px);
}
.course-title {
  font-weight: bold;
  font-size: 1.2rem;
  color: var(--text-heading, #000);
}
.course-desc {
  color: var(--text-body, #555);
}
section {
      padding: 60px 20px;
      max-width: 1100px;
      margin: 0 auto;
}
/* Reset + font */
body {
  margin: 0;
  font-family: Arial, sans-serif;
  line-height: 1.6;
  background-color: #f9f9f9;
  color: #333;
}

/* Consistent centered wrapper */
.page-wrapper {
  max-width: 900px;   /* keeps layout narrow for readability */
  margin: 0 auto;     /* centers horizontally */
  padding: 20px;
  background: #fff;
  min-height: 100vh;  /* ensures full screen height */
  display: flex;
  flex-direction: column;
}

/* Header, content, footer */
.site-header,
.site-footer {
  text-align: center;
  padding: 1rem;
  background: #eaeaea;
  border-radius: 12px;
  margin-bottom: 1rem;
}

.content {
  flex: 1; /* pushes footer to bottom */
  text-align: center; /* centers text */
}

/* Responsive typography */
h1 {
  font-size: clamp(1.8rem, 4vw, 2.5rem);
}
h2 {
  font-size: clamp(1.2rem, 3vw, 1.8rem);
}
p {
  font-size: clamp(1rem, 2.5vw, 1.2rem);
}

</style>
 <div class="page-wrapper">
    <header class="site-header">
      <h1>Welcome to Sharda Learning Center</h1>
    </header>

   

<div class="course-cards">
  <div class="course-card">
    <div class="course-title"><a href="/python-bootcamp/">Python Bootcamp</a></div>
    <div class="course-desc">Learn Python in 30 days by building real apps.</div>
  </div>
  <div class="course-card">
    <div class="course-title"><a href="/golang-bootcamp/">Golang Bootcamp</a></div>
    <div class="course-desc">Learn Go with backend-focused practical projects.</div>
  </div>
  <div class="course-card">
    <div class="course-title"><a href="/ai-ml-bootcamp/">AI/ML Bootcamp</a></div>
    <div class="course-desc">Kickstart your journey into Machine Learning with real-world datasets.</div>
  </div>
  <div class="course-card">
    <div class="course-title"><a href="/llm-bootcamp/">LLM Bootcamp</a></div>
    <div class="course-desc">Foundations, prompting, RAG, fine-tuning, and LLMOps curriculum.</div>
  </div>
  <div class="course-card">
    <div class="course-title"><a href="/2026/07/20/ai-llm-developer-roadmap.html">AI LLM Developer Roadmap Series</a></div>
    <div class="course-desc">Roadmap, first apps, fine-tuning/LLMOps, plus a full start-to-finish RAG capstone.</div>
  </div>
  <div class="course-card">
    <div class="course-title"><a href="/2026/07/23/advanced-document-knowledge-assistant-rag-project.html">Advanced: Document Knowledge Assistant</a></div>
    <div class="course-desc">Build a complete RAG product: ingest → retrieve → UI → API → Docker → eval.</div>
  </div>
  <div class="course-card">
    <div class="course-title"><a href="/cpp-stl/">C++ STL for Competitive Programming</a></div>
    <div class="course-desc">Hub + detailed pages: vector, iterators, map, set, heaps, algorithms, cheatsheet.</div>
  </div>
  <div class="course-card">
    <div class="course-title"><a href="/c-getting-started/">C Getting Started — Hands On</a></div>
    <div class="course-desc">Install, Hello World, variables, loops, arrays, pointers, strings, structs + mini projects.</div>
  </div>
</div>
  </div>
