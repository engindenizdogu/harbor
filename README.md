# Harbor - Knowledge Base

A personal knowledge base for Machine Learning topics, course notes, and technical documentation. Built with Jekyll and based on [Jekyll Garden](https://github.com/Jekyll-Garden/jekyll-garden.github.io).

## About

This site serves as an organized collection of notes from my studies in Machine Learning at Stevens Institute of Technology. Topics include:

- Machine Learning algorithms and concepts
- Math for ML (Linear Algebra, Probability, Statistics)
- Application design and programming
- Jekyll and web development notes
- Book summaries and reviews

The notes are written in Obsidian and published directly to GitHub Pages, with wiki-style `[[links]]` connecting related concepts.

### Wiki Links & Apostrophes

Obsidian sometimes converts straight apostrophes `'` to smart quotes `’` in `[[wiki links]]` (e.g. `[[Fisher’s Linear Discriminant]]`). The site now normalizes these characters client‑side so links resolve even if the stored note title uses a straight apostrophe (`Fisher's Linear Discriminant`). If you encounter a non‑resolving link, ensure it is wrapped in double brackets; the normalization will handle both `'` and `’`.

## Tech Stack

- **Jekyll** - Static site generator
- **Obsidian** - Note-taking and organization
- **GitHub Pages** - Hosting
- Built with Liquid, JavaScript, HTML, and CSS

## Local Development

```bash
bundle install
bundle exec jekyll serve
```

## Structure

- `_notes/Public/` - Published notes organized by topic
- `assets/` - CSS, images, and JavaScript
- `_layouts/` - Jekyll templates

## Credits

Based on [Jekyll Garden](https://github.com/Jekyll-Garden/jekyll-garden.github.io) theme.

## License

MIT License - use it freely for any project.
