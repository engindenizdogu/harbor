---
title: Robots.txt
tags: [web-development, software-engineering, seo, scraping]
draft: false
---
The `robots.txt` file is a standard text file placed at the root of a website (e.g., `https://example.com/robots.txt`) that tells automated web crawlers, spiders, and AI agents which pages or files they are allowed to request from the site.

## How it Works

It relies entirely on the **honor system**. It is a set of instructions and crawler etiquette, not a strict security firewall. A "polite" bot (like Googlebot) will read the file and respect the rules. A malicious scraper or rogue AI agent can easily ignore it.

### Syntax Example

```text
User-agent: *
Disallow: /admin/
Disallow: /private-data/

User-agent: GPTBot
Disallow: /

User-agent: Googlebot
Allow: /
Crawl-delay: 5
```

### Key Directives
- **`User-agent`**: Specifies which bot the rule applies to. `*` means all bots. Specific names can be targeted (e.g., `GPTBot` for OpenAI's crawler).
- **`Disallow`**: Tells the specified agent not to crawl a specific URL path.
- **`Allow`**: Overrides a `Disallow` directive for a specific subdirectory.
- **`Crawl-delay`**: Requests the bot to wait a specified number of seconds between requests to prevent server overload.
- **`Sitemap`**: Points the crawler to the XML sitemap to help it discover allowed pages efficiently.

## AI and Robots.txt
With the rapid rise of Generative AI, many publishers now update their `robots.txt` to explicitly block AI data scrapers from training on their content without permission. For example, adding `User-agent: GPTBot \n Disallow: /` asks OpenAI to stop indexing the site for model training purposes.
