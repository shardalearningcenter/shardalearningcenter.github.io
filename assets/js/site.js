(function () {
  var toggle = document.getElementById("nav-toggle");
  var nav = document.getElementById("site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  var tocToggle = document.getElementById("toc-toggle");
  var toc = document.getElementById("course-toc");
  if (tocToggle && toc) {
    tocToggle.addEventListener("click", function () {
      var open = toc.classList.toggle("is-open");
      tocToggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  // Auto-build TOC from h2/h3 if empty
  var tocNav = document.getElementById("course-toc-nav");
  var body = document.getElementById("course-body");
  if (tocNav && body) {
    if (!tocNav.children.length) {
      var heads = body.querySelectorAll("h2, h3");
      heads.forEach(function (h, i) {
        if (!h.id) {
          h.id =
            "section-" +
            (h.textContent || "s" + i)
              .toLowerCase()
              .replace(/[^a-z0-9]+/g, "-")
              .replace(/(^-|-$)/g, "");
        }
        if (h.tagName === "H2" || (h.tagName === "H3" && heads.length < 24)) {
          var a = document.createElement("a");
          a.href = "#" + h.id;
          a.textContent = (h.textContent || "").replace(/^[^\w]+/, "").trim();
          if (h.tagName === "H3") a.style.paddingLeft = "1rem";
          tocNav.appendChild(a);
        }
      });
    }

    var links = tocNav.querySelectorAll("a");
    function setActive() {
      var fromTop = window.scrollY + 120;
      var current = null;
      links.forEach(function (link) {
        var id = link.getAttribute("href").slice(1);
        var el = document.getElementById(id);
        if (el && el.offsetTop <= fromTop) current = link;
      });
      links.forEach(function (link) {
        link.classList.toggle("is-active", link === current);
      });
    }
    window.addEventListener("scroll", setActive, { passive: true });
    setActive();
  }
})();
