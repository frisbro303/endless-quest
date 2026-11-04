// Numbered theorem, lemma and definition boxes, styled by .thm in theme/style.css.
#let thm-counter = counter("thm")

#let thm-box(kind, name) = (body, title: none) => {
  thm-counter.step()
  html.elem("div", attrs: (class: "thm thm-" + kind))[
    *#name #context thm-counter.display()#if title != none [ (#title)].* #body
  ]
}

#let definition = thm-box("definition", "Definition")
#let lemma = thm-box("lemma", "Lemma")
#let theorem = thm-box("theorem", "Theorem")

#let inner(a, b) = $chevron.l #a, #b chevron.r$

// An equation in two layouts: `wide` on computers, `narrow` (line-broken) on phones; see .wide-only/.narrow-only in theme/style.css.
#let responsive(wide, narrow) = {
  html.elem("div", attrs: (class: "wide-only"), wide)
  html.elem("div", attrs: (class: "narrow-only"), narrow)
}

// The plain text of some content, for alt text; math and other non-text parts are dropped.
#let plain-text(it) = if type(it) == str { it } else if it.has("text") { it.text } else if it.has("children") {
  it.children.map(plain-text).join()
} else if it.has("body") { plain-text(it.body) } else if it == [ ] { " " } else { "" }

// A figure rendered for both themes: `name` is the path without extension; "name-dark.gif" is the dark version.
// One description: a string is alt text only (no caption); content is the caption, and its plain text the alt.
#let themed-gif(name, description, alt: auto) = {
  let caption = if type(description) == str { none } else { description }
  let alt = if alt != auto { alt } else { plain-text(description) }
  figure(
  {
    html.elem("img", attrs: (src: name + ".gif", alt: alt, class: "light-only"))
    html.elem("img", attrs: (src: name + "-dark.gif", alt: alt, class: "dark-only"))
  },
  caption: caption,
  )
}
