---
layout: page
title: Courses
permalink: /courses/
---

<style>
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
</style>

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
</div>
