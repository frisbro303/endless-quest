// Loaded as a blocking script in <head> so the page never flashes the wrong theme.
(function () {
  var root = document.documentElement;
  var saved = null;
  try { saved = localStorage.getItem("theme"); } catch (e) {}
  var dark = saved ? saved === "dark" : matchMedia("(prefers-color-scheme: dark)").matches;
  root.dataset.theme = dark ? "dark" : "light";

  document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("theme-toggle").addEventListener("click", function () {
      var next = root.dataset.theme === "dark" ? "light" : "dark";
      root.dataset.theme = next;
      try { localStorage.setItem("theme", next); } catch (e) {}
    });

    // Clicking a figure's GIF freezes it on the current frame; clicking again plays it.
    document.addEventListener("click", function (e) {
      var img = e.target.closest("figure img");
      if (!img) return;
      if (img.dataset.gif) { img.src = img.dataset.gif; delete img.dataset.gif; return; }
      var canvas = document.createElement("canvas");
      canvas.width = img.naturalWidth; canvas.height = img.naturalHeight;
      canvas.getContext("2d").drawImage(img, 0, 0);
      img.dataset.gif = img.src; img.src = canvas.toDataURL();
    });
  });
})();
