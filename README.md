# Jekyll Garden
![screenshot](https://github.com/user-attachments/assets/f5752b1a-eb11-4385-a2ad-09f0e698ad30)
A simple Jekyll theme that turns your Obsidian notes into a beautiful website. Perfect for sharing your thoughts and knowledge online. If you use Obsidian for note-taking, this theme makes it easy to publish your markdown files as a connected website with wiki-style links and full-text search.

### What it does

Jekyll Garden connects your notes together with simple `[[note title]]` links, just like in Obsidian. You can find any note quickly with the built-in search that works as you type. The design focuses on your content with a clean, minimal look that works great on phones, tablets, and computers. Dark theme support is optional (UI toggle removed by default in this fork). The theme also supports mathematical expressions if you need to write equations.

## Getting Started

Getting started is straightforward. First, download this theme to your computer. Then edit the settings in the `_config.yml` file with your website information. Add your notes to the `_notes` folder, and finally deploy to GitHub Pages, Netlify, or any web hosting service.

### Add Your First Note

Create a file under `_notes/Public/`:

```yaml
---
title: "My First Note"
date: 2024-01-15
feed: "show"
---
```

Write content in Markdown and connect ideas using `[[Wiki Links]]`.

## Basic Setup

Edit `_config.yml` with your information:

```yaml
title: "My Website"
heading: "Your Name"
description: "A brief description of your site"
url: "https://yoursite.com"
```

### Obsidian Setup

Use the `_notes` folder as your Obsidian vault for a seamless write→publish flow.

- Front matter per note:
	```yaml
	---
	title: "Your Note Title"
	date: 2024-01-15
	feed: "show"   # or "hide" for private notes
	---
	```
- Recommended `.gitignore` entries:
	```gitignore
	.obsidian/
	.trash/
	_site/
	.sass-cache/
	.jekyll-cache/
	```
- Keep private notes out of the site by placing them under a separate folder (e.g. `_notes/Private/`) and ignoring it, or by setting `feed: "hide"`.

Workflow: write notes in Obsidian → use `[[Wiki Links]]` → commit and push → site updates.

### Deployment Options

You can deploy your site to a subdomain (like `notes.yoursite.com`) or a subdirectory (like `yoursite.com/notes`):

**For subdomains:**
```yaml
url: "https://notes.yoursite.com"
baseurl: ""
```

**For subdirectories:**
```yaml
url: "https://yoursite.com"
baseurl: "/notes"
```

See `SUBDOMAIN_SETUP.md` for more details.

## Writing Notes

### Creating a Note

Each note is just a markdown file with a title. You write your content in markdown format, just like you would in Obsidian or any other markdown editor.

```yaml
---
title: "My First Note"
date: 2025-01-15
---
```

### Adding Photos
Example: ![](/assets/img/dot_prod.png)

## Features

### Linking Notes Together
Connect your notes by using `[[note title]]` to link to other notes. This creates the same kind of connections you're used to in Obsidian, but now they work on your website too.


### Simple Linking
The linking system works just like Obsidian:

- Internal: `[[Note Title]]`
- External: `[[Google::https://google.com]]`
- Example:
	```markdown
	This note connects to [[Getting Started]] and [[Markdown Guide]].
	For more information, check out [[Jekyll::https://jekyllrb.com]].
	```

Backlinks are automatic: when a note links to another, the linked note shows a Backlinks section.

Troubleshooting wiki links:
- Ensure the target note exists under `_notes/`
- Match the title exactly
- Set `feed: "show"` in front matter for published notes

### Search
Finding content is easy with the built-in search. It searches through all your notes instantly as you type, looking at both titles and content to help you find exactly what you need.

### Hierarchical Sidebar
Organize your notes inside `_notes/Public/` using subfolders. Each first-level subfolder becomes a collapsible section in the left sidebar. Notes placed directly under `Public/` appear after the folders. Example:

```
_notes/
	Public/
		Math/
			Derivatives.md
			Integrals.md
		Programming/
			Python Tips.md
		Inbox.md   # root-level note
```

This will render two folder groups (Math, Programming) followed by the root-level note (Inbox). Folders use native `<details>` / `<summary>` for zero‑JS toggling.

### Backlinks
See which notes link to the current one you're reading. This helps you discover related content and explore the connections between your ideas, just like the backlinks feature in Obsidian.

### Math
If you need to write mathematical expressions, the theme supports it. Use `$x = y$` for inline math and `$$\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}$$` for complex equations.

### Blog Integration
Write chronological posts under `_posts/` in standard Jekyll format. Posts coexist with evergreen notes and can link to them.

## How to Publishing Your Site

### GitHub Pages (Free)
GitHub Pages is the easiest way to get started. Upload your files to GitHub, enable GitHub Pages in the repository settings, and your site goes live automatically.

### Netlify (Free)
Netlify is another great option. Connect your GitHub repository to Netlify, and it will build and host your site. Every time you update your files, your site updates automatically.

### Local Testing
Test your site locally before publishing:

```bash
bundle install
bundle exec jekyll serve
```

### Customization
Change the look of your site by editing the `assets/css/style.css` file. You can modify colors, fonts, and other visual elements to match your preferences. If you want to customize the layout, you can modify files in the `_layouts/` folder. Add your own CSS and JavaScript as needed, but remember to keep it simple.

#### Site Configuration (`_config.yml`)

Basic settings:
```yaml
title: "My Digital Garden"
heading: "Your Name"
description: "A brief description of your site"
url: "https://yoursite.com"
```

Menu items:
```yaml
menu:
	- title: "Notes"
		url: "/notes"
	- title: "About"
		url: "/about"
	- title: "Blog"
		url: "/blog"
```

Preferences:
```yaml
preferences:
	homepage:
		enabled: true      # Show custom homepage
	search:
		enabled: true      # Enable search
	backlinks:
		enabled: true      # Show backlinks
```

Colors and fonts (CSS):
```css
:root {
	--primary-color: #007acc;
	--text-color: #333;
	--background-color: #fff;
	--font-family: -apple-system, BlinkMacSystemFont, sans-serif;
}
```

Dark mode: The UI toggle is intentionally removed in this fork. You can re‑introduce a toggle in your layout and switch `data-theme` via JavaScript if desired.

Custom fonts:
```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

:root {
	--font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}
```

#### Homepage background image
Disabled by default in this fork. If you want a homepage background image, add a `body.home` rule in `assets/css/style.css` with your `background-image` and place the asset under `assets/img/`.

#### Markdown Cheatsheet

Headings:
```markdown
# Main heading
## Section heading
### Subsection heading
```

Text formatting:
```markdown
*Italic* _italic_  **Bold** __bold__  `inline code`  ~~strike~~
```

Lists:
```markdown
- Item
- Nested
  - Child

1. First
2. Second
```

Links:
```markdown
[External](https://example.com)
[[Wiki link]]
[[External link::https://example.com]]
```

Code blocks:
```markdown
```javascript
function hello() {
  console.log("Hello, World!");
}
```
```

Blockquotes:
```markdown
> This is a blockquote.
> It can span multiple lines.
```

Tables:
```markdown
| Header | Header |
|--------|--------|
| Cell   | Cell   |
```

Math (KaTeX):
```markdown
Inline: $x = y$
Block: $$\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}$$
```

## Contributing
Found a bug or have an idea for improvement? Contributions are welcome. Fork the repository, make your changes, and submit a pull request.

## License

MIT License - use it freely for any project.
