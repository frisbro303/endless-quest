// The blog, built with tdg (github.com/frisbro303/tdg): its widgets first (Rust, compiled to WebAssembly), then
// the site and its posts' PDFs, each by one Typst compile (a page in both would have each of its labels twice),
// and the CV's PDF, a document of its own:
//
//   cargo wgw   (cargo install --git https://github.com/frisbro303/wgw cargo-wgw)
//   typst compile --features html,bundle --format bundle site.typ _site
//   typst compile --features html,bundle --format bundle --input tdg=pdf site.typ _site
//   typst compile pages/cv.typ _site/about/cv.pdf
//
// serve.py does all four, and again whenever something changes.
#import "/template.typ": *

#show: site.with(
  title: "Endless Quest",
  author: "Felix Granum",
  icon: path("theme/icon.png"),
  nav: (("blog", ""), ("about/cv", "about/")),
  footer: (links: (email: "mailto:felix.granum@pm.me", github: "https://github.com/frisbro303")),
)

#include "index.typ"
#include "posts/hopf-fibrations/main.typ"
#include "pages/about.typ"
