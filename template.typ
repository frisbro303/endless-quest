// The blog's Typst: tdg's site templates and components (github.com/frisbro303/tdg), and a few of its own. Posts
// import this, and start with `#show: post.with(...)`.
#import "@local/tdg:0.2.0": *

#let inner(a, b) = $chevron.l #a, #b chevron.r$

// Text for the web version only, such as how to use an interactive figure.
#let web(body) = context if target() != "paged" { body }
