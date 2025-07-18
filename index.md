---
layout: home
title: Welcome
---
  <style>
    * { box-sizing: border-box; }
    .body1 {
      margin: 0;
      font-family: 'Segoe UI', sans-serif;
      background: #f9f9f9;
      color: #333;
      scroll-behavior: smooth;
    }

    /* TOP CTA */
    .top-cta {
      background: #ff9900;
      color: #fff;
      text-align: center;
      padding: 14px 20px;
      font-size: 18px;
      font-weight: bold;
    }

    .top-cta a {
      color: #fff;
      text-decoration: underline;
    }

    /* NAVBAR */
    nav {
      background-color: #0a66c2;
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 10px 30px;
      position: sticky;
      top: 0;
      z-index: 1000;
    }

    nav h2 {
      color: #fff;
      margin: 0;
      font-size: 22px;
    }

    nav ul {
      list-style: none;
      display: flex;
      gap: 20px;
      margin: 0;
      padding: 0;
    }

    nav ul li a {
      text-decoration: none;
      color: #fff;
      font-weight: bold;
      transition: color 0.3s;
    }

    nav ul li a:hover {
      color: #ffcc00;
    }

    header {
      background-color: #0a66c2;
      color: #fff;
      padding: 60px 20px;
      text-align: center;
    }

    header h1 {
      font-size: 42px;
      margin-bottom: 10px;
    }

    header p {
      font-size: 20px;
      max-width: 720px;
      margin: 0 auto;
    }

    .cta-section {
      text-align: center;
      margin-top: 30px;
    }

    .cta-section a {
      text-decoration: none;
      background: #ff9900;
      color: #fff;
      padding: 14px 30px;
      border-radius: 8px;
      font-weight: bold;
      font-size: 18px;
      box-shadow: 0 4px 8px rgba(0,0,0,0.15);
      transition: background 0.3s;
    }

    .cta-section a:hover {
      background: #e67e00;
    }

    section {
      padding: 60px 20px;
      max-width: 1100px;
      margin: 0 auto;
    }

    h2 {
      text-align: center;
      font-size: 32px;
      margin-bottom: 40px;
      color: #0a66c2;
    }

    .features {
      display: flex;
      flex-wrap: wrap;
      gap: 30px;
      justify-content: center;
    }

    .feature {
      background: #fff;
      padding: 30px;
      border-radius: 12px;
      flex: 1 1 280px;
      box-shadow: 0 0 15px rgba(0,0,0,0.05);
      transition: transform 0.3s;
    }

    .feature:hover {
      transform: translateY(-5px);
    }

    .feature h3 {
      margin-top: 0;
      color: #0a66c2;
    }

    footer {
      text-align: center;
      padding: 30px;
      background: #eee;
      font-size: 14px;
      color: #666;
    }

    @media (max-width: 768px) {
      nav {
        flex-direction: column;
        align-items: flex-start;
      }

      nav ul {
        flex-direction: column;
        width: 100%;
        gap: 10px;
        padding-left: 0;
      }

      header h1 {
        font-size: 30px;
      }

      section {
        padding: 40px 10px;
      }
    }
 </style>
 <div class="body1">
  <div class="top-cta">
    🚀 Ready to Learn AI & Programming from Engineers Who've Built for Millions?
    <a href="https://youtube.com/@YourChannelName" target="_blank">Start Now</a>
  </div>

  <!-- NAVBAR - ->
  <nav>
    <h2>Sharda Learning Center</h2>
    <ul>
      <li><a href="#home">Home</a></li>
      <li><a href="#about">About</a></li>
      <li><a href="#courses">Courses</a></li>
      <li><a href="/blog">Blog</a></li>
      <li><a href="#contact">Contact</a></li>
      <li><a href="#socials">Socials</a></li>
    </ul>
  </nav>

  <!-- HERO SECTION -->
  <header id="home">
    <h1>Learn Programming & AI from Real Engineers</h1>
    <p>Built by ex-Walmart, Microsoft & VMware employees — our mission is to make coding and AI simple, project-based, and fun for everyone.</p>
    <div class="cta-section">
      <a href="https://youtube.com/@ShardaLearningCenter" target="_blank">🚀 Visit Our YouTube Channel</a>
    </div>
  </header>

  <!-- ABOUT -->
  <section id="about">
    <h2>💼 Why Learn With Us?</h2>
    <div class="features">
      <div class="feature">
        <h3>👨‍💻 Real Industry Experience</h3>
        <p>We bring insights from Big Tech—so you learn how real software is built, not just textbook concepts.</p>
      </div>
      <div class="feature">
        <h3>🧠 AI & Programming Made Easy</h3>
        <p>From Python to Deep Learning, we simplify complex tech into practical, beginner-friendly lessons.</p>
      </div>
      <div class="feature">
        <h3>🎓 For Students & Professionals</h3>
        <p>Whether you're just starting or switching careers, we help you go from zero to hired with confidence.</p>
      </div>
    </div>
  </section>

  <!-- COURSES -->
  <section id="courses">
    <h2>🚀 Explore Our Most-Loved Courses</h2>
    <div class="features">
      <div class="feature">
        <h3>🔥 Master Python in 10 Days</h3>
        <p>From zero to expert: Learn Python with hands-on coding challenges and real-world projects.</p>
      </div>
      <div class="feature">
        <h3><a href="/llm-bootcamp/">AI, Large language models bootcamp,🤖 Build AI Projects Like a Pro</a></h3>
        <p>Create chatbots, recommendation systems, and machine learning models using real datasets.</p>
      </div>
      <div class="feature">
        <h3>🧠 Crack DSA for Tech Interviews</h3>
        <p>Master Data Structures & Algorithms with live coding sessions and pattern-based questions.</p>
      </div>
      <div class="feature">
        <h3>🌐 Full-Stack Web Development</h3>
        <p>Build apps using HTML, CSS, JavaScript, React, and Node.js. Learn by launching your own mini-startups.</p>
      </div>
      <div class="feature">
        <h3>🚀 Machine Learning for Beginners</h3>
        <p>Understand ML step-by-step with Python, scikit-learn, and projects like image classifiers.</p>
      </div>
      <div class="feature">
        <h3>📊 SQL & Data Analytics Bootcamp</h3>
        <p>Write powerful queries, analyze data, and create dashboards that drive business decisions.</p>
      </div>
    </div>
  </section>

  <!-- BLOG -->
  <section id="blog">
    <h2>📚 From the Blog</h2>
    <div class="features">
      <div class="feature">
        <h3>🧩 How AI Will Change Jobs in 2025</h3>
        <p>We break down what AI disruption really means for you and how to future-proof your career.</p>
      </div>
      <div class="feature">
        <h3>👨‍🏫 How We Teach Code Differently</h3>
        <p>Learn why our step-by-step method works better than endless tutorials and theory-heavy courses.</p>
      </div>
    </div>
  </section>

  <!-- CONTACT -->
  <!-- <section id="contact">
    <h2>📬 Contact Us</h2>
    <p style="text-align:center;">For partnerships, business inquiries or support, reach us at
      <a href="mailto:your@email.com">
        your@email.com
      </a>
    </p>
  </section> -->

  <!-- SOCIALS -->
  <section id="socials">
    <h2>🌐 Follow Us</h2>
    <p style="text-align:center;">
      <a href="https://www.youtube.com/@ShardaLearningCenter" target="_blank">YouTube</a> |
      <a href="https://linkedin.com/company/sharda-learning-center" target="_blank">LinkedIn</a> |
      <a href="https://twitter.com/vcluevion" target="_blank">Twitter</a> |
      <a href="https://github.com/shardalearningcenter/shardalearningcenter-code" target="_blank">GitHub</a>
      <a href="https://chat.whatsapp.com/Kx0hL4UYAB80tVApsLXZSf?mode=r_t">WhatsApp Channel</a>
    </p>
  </section>
</div>
