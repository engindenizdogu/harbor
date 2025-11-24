---
title: Notes
---
# What is Jekyll?
Jekyll is a **static site generator**. It processes your site by converting Markdown files into static HTML. Jekyll uses the [Liquid](https://shopify.github.io/liquid/) templating language to process templates. Any files or folders that **don't** start with an underscore (`_`) are copied verbatim to the `_site` output folder when you build your site.

Example folder structure:
```
my-jekyll-site
├── _data
├── _includes
├── _layouts
├── _posts 
├── _site
├── _config.yml
├── Gemfile
├── assets
	├── css
	│    └── main.css
    ├── images
    │    └── logo.png
    └── js 
         └── scripts.js
├── index.html (could also be an .md file)
└── about.md
```

> **Gemfile (publishing with GitHub)**
> If publishing your site with GitHub Pages, you can match production version of Jekyll by using the `github-pages` gem instead of `jekyll` in your `Gemfile`. In this scenario you may also want to exclude `Gemfile.lock` from your repository because GitHub Pages ignores that file.

# Useful Links
- [Quickstart - Jekyll • Simple, blog-aware, static sites](https://jekyllrb.com/docs/)
- [Liquid template language](https://shopify.github.io/liquid/)
- [The Liquid Sandbox](https://jumpseller.com/support/liquid-sandbox/)

# Themes I Like
* [sighingnow/jekyll-gitbook: Build Jekyll site with GitBook style!](https://github.com/sighingnow/jekyll-gitbook)
* [just-the-docs/just-the-docs: A modern, high customizable, responsive Jekyll theme for documentation with built-in search.](https://github.com/just-the-docs/just-the-docs)

# Alternatives
HUGO is an alternative framework I found along the way. Might try to use it later on.
* Documentation: [The world's fastest framework for building websites](https://gohugo.io/)
* A simple HUGO theme: [Book](https://themes.gohugo.io/themes/hugo-book/)
* [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)

> Advice from the Obsidian Team itself (on hosting .md files) 🙂
> [Link to Reddit post...](https://www.reddit.com/r/ObsidianMD/comments/16e5jek/comment/jzv38ja/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button)i

