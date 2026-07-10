(function () {
  var toggle = document.getElementById("nav-toggle");
  var nav = document.getElementById("site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  var sideToggle = document.getElementById("sidenav-toggle");
  var sidenav = document.getElementById("docs-sidenav");
  if (sideToggle && sidenav) {
    sideToggle.addEventListener("click", function () {
      var open = sidenav.classList.toggle("is-open");
      sideToggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  } else if (sideToggle && !sidenav) {
    sideToggle.style.display = "none";
  }

  var tocToggle = document.getElementById("toc-toggle");
  var toc = document.getElementById("course-toc");
  if (tocToggle && toc) {
    tocToggle.addEventListener("click", function () {
      var open = toc.classList.toggle("is-open");
      tocToggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  var tocNav = document.getElementById("course-toc-nav");
  var body =
    document.querySelector(".docs-content") ||
    document.getElementById("course-body");
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
          if (h.tagName === "H3") a.style.paddingLeft = "12px";
          tocNav.appendChild(a);
        }
      });
    }

    var links = tocNav.querySelectorAll("a");
    function setActive() {
      var fromTop = window.scrollY + 100;
      var current = null;
      links.forEach(function (link) {
        var id = (link.getAttribute("href") || "").slice(1);
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

  // Mark current top-nav link
  var path = location.pathname.replace(/\/$/, "") || "/";
  document.querySelectorAll(".nav-links a").forEach(function (a) {
    var href = (a.getAttribute("href") || "").replace(/\/$/, "") || "/";
    if (href === path) a.setAttribute("aria-current", "page");
  });
})();
