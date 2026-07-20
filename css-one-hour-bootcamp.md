---
layout: page
title: 1-Hour CSS Bootcamp
permalink: /css-one-hour-bootcamp/
---

# 1-Hour CSS Bootcamp — Minimal Expertise

Go from **zero → useful CSS** in about **60 minutes**.  
No design theory. Only what you need to style real pages.

**You need:** a browser + any editor (VS Code / Cursor)  
**Related:** [Courses](/courses/) · [Frontend Roadmap](/2025/07/09/frontend-developer-roadmap.html) · [C Getting Started](/c-getting-started/)

---

## Timer Plan

| Minutes | Focus |
|---|---|
| 0–5 | Setup + how CSS attaches |
| 5–15 | Selectors |
| 15–25 | Box model + spacing |
| 25–35 | Text & colors |
| 35–45 | Flexbox (layout superpower) |
| 45–55 | Responsive + mini page |
| 55–60 | Cheatsheet review |

---

## Minute 0–5 — Setup

Create three files in one folder:

`index.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>1-Hour CSS</title>
  <link rel="stylesheet" href="styles.css" />
</head>
<body>
  <header class="site-header">
    <h1 id="title">CSS in 1 Hour</h1>
    <p class="tagline">Build · Style · Ship</p>
  </header>

  <main class="container">
    <section class="card">
      <h2>Card One</h2>
      <p>I will look better after CSS.</p>
      <a class="btn" href="#">Learn more</a>
    </section>
    <section class="card">
      <h2>Card Two</h2>
      <p>Flexbox will place us side by side.</p>
      <a class="btn btn-outline" href="#">Docs</a>
    </section>
  </main>

  <footer class="site-footer">You did it.</footer>
</body>
</html>
```

`styles.css` — start empty; fill as you go.

Open `index.html` in the browser. Hard-refresh after each change.

---

## Minute 5–15 — Selectors (target elements)

```css
/* element */
h1 { }

/* class (reuse) */
.card { }

/* id (one unique thing) */
#title { }

/* descendant */
.container p { }

/* group */
h1, h2, .tagline { }
```

**Add this now:**

```css
body {
  margin: 0;
  font-family: Georgia, "Times New Roman", serif;
  background: #f4f7fb;
  color: #1a1a1a;
}

.site-header {
  background: #0a66c2;
  color: #fff;
  padding: 1.5rem;
}

.tagline {
  opacity: 0.9;
}
```

### Quick rules
- Prefer **classes** for styling  
- IDs are for unique hooks  
- Specificity: `id` > `class` > `element`

### Task (2 min)
Style `h2` inside `.card` to be blue (`#0a66c2`).

---

## Minute 15–25 — Box Model (spacing that doesn’t break)

Everything is a box:

```text
margin  → outside gap
border  → edge
padding → inner gap
content → text/image
```

```css
.container {
  max-width: 900px;
  margin: 1.5rem auto;
  padding: 0 1rem;
}

.card {
  background: #fff;
  border: 1px solid #d9e2ec;
  border-radius: 12px;
  padding: 1.25rem;
  margin-bottom: 1rem;
  box-sizing: border-box;
}

/* Do this once globally — saves pain */
*,
*::before,
*::after {
  box-sizing: border-box;
}
```

### Margin vs padding
| Use | When |
|---|---|
| `padding` | Space inside the card |
| `margin` | Space between cards |

### Task (2 min)
Give `.site-footer` padding and centered gray text.

---

## Minute 25–35 — Text, Color, Buttons

```css
h1, h2 {
  line-height: 1.2;
  margin-top: 0;
}

p {
  line-height: 1.6;
  color: #334;
}

.btn {
  display: inline-block;
  padding: 0.6rem 1rem;
  background: #0a66c2;
  color: #fff;
  text-decoration: none;
  border-radius: 8px;
  border: 2px solid #0a66c2;
  font-weight: 700;
}

.btn:hover {
  background: #084e96;
  border-color: #084e96;
}

.btn-outline {
  background: transparent;
  color: #0a66c2;
}

.btn-outline:hover {
  background: #0a66c2;
  color: #fff;
}
```

### Units you’ll actually use
| Unit | Use for |
|---|---|
| `rem` | Font / spacing (scalable) |
| `%` | Width of parent |
| `px` | Borders, fine tweaks |
| `vh/vw` | Full viewport tricks |

### Task (2 min)
Make `.tagline` italic and slightly smaller (`0.95rem`).

---

## Minute 35–45 — Flexbox (layout in 10 minutes)

Flexbox = one-dimensional layout (row or column).

```css
.container {
  max-width: 900px;
  margin: 1.5rem auto;
  padding: 0 1rem;
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.card {
  background: #fff;
  border: 1px solid #d9e2ec;
  border-radius: 12px;
  padding: 1.25rem;
  margin-bottom: 0;
  flex: 1 1 260px; /* grow | shrink | basis */
}
```

### Flex cheat phrases
```css
display: flex;
justify-content: center; /* main axis */
align-items: center;     /* cross axis */
gap: 1rem;
flex-direction: column;
```

Header with space-between (pattern):

```css
.site-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.5rem;
}
```

### Task (3 min)
Make header a flex row with title on the left and tagline on the right (on wide screens).

---

## Minute 45–55 — Responsive + Polish

```css
.site-footer {
  text-align: center;
  color: #667;
  padding: 2rem 1rem;
  font-size: 0.9rem;
}

/* Mobile first tweak */
@media (max-width: 600px) {
  .site-header {
    flex-direction: column;
    align-items: flex-start;
  }

  h1 {
    font-size: 1.6rem;
  }
}
```

### Mini “expertise” checklist — finish these
- [ ] Page has header, 2 cards, footer  
- [ ] Cards sit in a responsive flex row  
- [ ] Buttons have hover states  
- [ ] Looks OK on a narrow phone width  

**Stretch (optional):** add a third card and a simple nav with flex `gap`.

---

## Minute 55–60 — Cheatsheet (keep this)

```css
/* Reset-ish */
* { box-sizing: border-box; }
body { margin: 0; }

/* Center page */
.wrap { max-width: 900px; margin: 0 auto; padding: 0 1rem; }

/* Card */
.card {
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 12px;
  padding: 1rem;
}

/* Button */
.btn {
  display: inline-block;
  padding: .6rem 1rem;
  background: #0a66c2;
  color: #fff;
  border-radius: 8px;
  text-decoration: none;
}

/* Flex row */
.row { display: flex; flex-wrap: wrap; gap: 1rem; }
.row > * { flex: 1 1 250px; }

/* Responsive */
@media (max-width: 600px) {
  .row { flex-direction: column; }
}
```

### Debug tip
Right-click → **Inspect** → check box model and computed styles. This is how pros learn faster.

---

## You’re “minimally expert” if you can…

1. Attach a CSS file and use class selectors  
2. Control spacing with margin/padding + `box-sizing`  
3. Style links as buttons with `:hover`  
4. Lay out cards with **flexbox**  
5. Add one `@media` query for mobile  

That’s enough to style landing sections, blogs, and bootcamp pages.

---

## Next (after the hour)

| Next skill | Why |
|---|---|
| CSS Grid | 2D page layouts |
| Custom properties (`--brand`) | Themes in one place |
| Forms styling | Real product UI |
| Full path | [Frontend Developer Roadmap](/2025/07/09/frontend-developer-roadmap.html) |

### 15-minute follow-up project
Rebuild this site’s course card grid with only flex + your own colors (no copy-paste from browser).

---

## Full starter CSS (if you got stuck)

Paste into `styles.css` and compare with yours:

```css
*,
*::before,
*::after { box-sizing: border-box; }

body {
  margin: 0;
  font-family: Georgia, "Times New Roman", serif;
  background: #f4f7fb;
  color: #1a1a1a;
}

.site-header {
  background: #0a66c2;
  color: #fff;
  padding: 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.tagline {
  margin: 0;
  font-style: italic;
  font-size: 0.95rem;
  opacity: 0.9;
}

.container {
  max-width: 900px;
  margin: 1.5rem auto;
  padding: 0 1rem;
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.card {
  background: #fff;
  border: 1px solid #d9e2ec;
  border-radius: 12px;
  padding: 1.25rem;
  flex: 1 1 260px;
}

.card h2 {
  color: #0a66c2;
  margin-top: 0;
}

p { line-height: 1.6; color: #334; }

.btn {
  display: inline-block;
  padding: 0.6rem 1rem;
  background: #0a66c2;
  color: #fff;
  text-decoration: none;
  border-radius: 8px;
  border: 2px solid #0a66c2;
  font-weight: 700;
}

.btn:hover { background: #084e96; border-color: #084e96; }

.btn-outline {
  background: transparent;
  color: #0a66c2;
}

.btn-outline:hover {
  background: #0a66c2;
  color: #fff;
}

.site-footer {
  text-align: center;
  color: #667;
  padding: 2rem 1rem;
  font-size: 0.9rem;
}

@media (max-width: 600px) {
  .site-header {
    flex-direction: column;
    align-items: flex-start;
  }
  h1 { font-size: 1.6rem; }
}
```

---

*One hour. One page. Flex + box model + hover. That is minimal CSS expertise.*
