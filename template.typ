// The Endless Quest theme: tdg's blog look (github.com/frisbro303/tdg) with the blog's own stylesheet, and the
// blog's templates. Pages import this, and start with one: `#show: post.with(...)`, `home.with(...)` or
// `standalone.with(...)`.
#import "@local/tdg:0.1.0": *

/// The blog's look, which its templates share: tdg's blog look, with theme/style.css instead of its stylesheet.
#let look = blog.look + (css: (path("theme/style.css"),))

/// A post: at posts/<slug>/, dated, and also a PDF. Its settings: `date` and `updated` ("YYYY-MM-DD"), shown beside
/// it. The home page lists the posts with `#listing("post")`.
#let post = template("post", ..look,
  url: slug => "posts/" + slug + "/",
  fields: (date: none, updated: none),
  required: ("date",),
  prepare: page => page + (date: to-date(page.date), updated: if page.updated != none { to-date(page.updated) }),
  header: post-header,
  pdf-header: pdf-title,
  pdf: true,
)

/// The home page: the site's front page, for listings.
#let home = template("home", ..look, url: slug => "", main: (site, page, body) => body, class: "home")

/// A page that isn't a post, such as the about page: no footer; it lays out its own headings.
#let standalone = template("page", ..look, header: page => none, footer: false)

#let inner(a, b) = $chevron.l #a, #b chevron.r$

// Text for the web version only, such as how to use an interactive figure.
#let web(body) = context if target() != "paged" { body }
