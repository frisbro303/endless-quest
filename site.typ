// The blog, built with tdg (github.com/frisbro303/tdg): its widgets first (Rust, compiled to WebAssembly), then
// the site and its PDFs, each by one Typst compile (a page in both would have each of its labels twice):
//
//   cargo wgw   (cargo install --git https://github.com/frisbro303/wgw cargo-wgw)
//   typst compile --features html,bundle --format bundle site.typ _site
//   typst compile --features html,bundle --format bundle --input tdg=pdf site.typ _site
//
// serve.py does all three, and again whenever something changes.
#import "/template.typ": *

#show: site.with(
  title: "Endless Quest",
  author: "Felix Granum",
  icon: path("theme/icon.png"),
  css: (path("theme/style.css"),),
  theme-style: false,  // the blog's own stylesheet, instead of tdg's blog theme's
  nav: (("blog", ""), ("about/cv", "cv/")),
  footer: (links: (email: "mailto:felix.granum@pm.me", github: "https://github.com/frisbro303")),
  home: "blog",
)

#include "posts/hopf-fibrations/main.typ"
#include "pages/cv.typ"
