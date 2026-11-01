# Endless Quest

Add a post to `posts/` and push to `main`; it is published to [frisbro303.github.io/endless-quest](https://frisbro303.github.io/endless-quest/).
Dragging files or a folder into GitHub's "Upload files" page works too.

- **Single file:** `posts/my-post.typ` becomes `/posts/my-post/`
- **Folder with figures or data:** `posts/my-post/main.typ` becomes `/posts/my-post/`. The file can
  have any name if it is the only `.typ` file in the top level of the folder. Everything else in
  the folder is published next to the page, so `#link("data.csv")` works.

Metadata is optional:

```typst
#set document(title: "My Post", description: "Shown on the front page.")
```

Without a title, the file or folder name is used. The date is always the post's first commit.

Non-text content such as shapes or plots needs wrapping to appear in HTML export:
`#html.frame(rect(...))`. Images work as usual.

Files in `pages/` work the same way but are standalone pages rather than posts: `pages/cv.typ`
becomes `/cv/`, gets a link in the site navigation, and is also published as a PDF. They must
compile to PDF as well as HTML, and can branch on `target()` where the two should differ.

The site name, front-page intro and links are at the top of `build.py`; the theme is in `theme/`.

Preview locally with `python3 build.py && python3 -m http.server -d _site`. Requires Typst 0.15;
the version CI uses is pinned in `.github/workflows/publish.yml`.

If a post fails to compile, the deploy is skipped and the current site stays up.
