---
title: NES.css
tags: [software, css, quartz, frontend, ui, retro, 8-bit, resource]
draft: false
---

**NES.css** is a NES-style (8-bit) CSS Framework. It provides a blocky, pixel-art aesthetic reminiscent of the 1980s Nintendo Entertainment System interface. Combining technical learning with a passion for retro aesthetics, it allows you to build pixel-perfect retro dashboards, speech bubbles, and retro status icons directly in your digital garden.

Source: [NES.css Demo](https://nostalgic-css.github.io/NES.css/) | [GitHub Repository](https://github.com/nostalgic-css/NES.css) | [Medium Article (Backstory)](https://medium.com/@bc_rikko/why-i-created-and-released-nes-css-ee8966bacd09)

## Core Overview
* **Aesthetic:** Retro 8-bit design.
* **Tech Stack:** CSS-only (JavaScript-free). No dependencies required.
* **Usage:** Simply add class names to HTML elements to apply styles.
* **Font Recommendation:** Best used with the **"Press Start 2P"** font from Google Fonts.

---

## Google Font Configuration

NES.css is designed to be paired with the **Press Start 2P** 8-bit style Google Font. Since Quartz has a built-in font loader, you can load and configure this font directly in `quartz.config.ts`.

Because "Press Start 2P" only supports a font weight of `400`, specify the weights array explicitly to prevent Google Fonts from returning errors or missing weights:

```typescript
      typography: {
        header: {
          name: "Press Start 2P",
          weights: [400],
        },
        body: "Roboto",
        code: {
          name: "Press Start 2P",
          weights: [400],
        },
      },
```

---

## Stylesheet Integration Options

Depending on your design goals, you can choose one of three methods to integrate NES.css into Quartz.

### Option 1: Surgical Icon-Only Integration (Recommended)

If you only want to use the retro social media and status icons **without** letting NES.css overwrite your website's custom fonts, colors, standard buttons, or global cursors:

1. Install the `nes.css` dependency:
   ```bash
   npm install nes.css
   ```

2. Add base color variables and surgically import only the icon mixins and icon styles inside `quartz/styles/custom.scss`:
   ```scss
   // Define base retro colors needed by icons (prevents global reset imports)
   $color-black: #212529;
   $base-color: $color-black;

   // Import ONLY the icon mixins and icon styles from NES.css (ignores all global overrides/cursors)
   @import "nes.css/scss/utilities/icon-mixin";
   @import "nes.css/scss/icons/icons";
   @import "nes.css/scss/pixel-arts";
   ```

This compiles only the `.nes-icon` class definitions and bundles their corresponding pixel-art matrices, ensuring all your site's default fonts, styles, and cursors remain completely untouched.

### Option 2: Full NPM Integration (Self-Hosted Framework)

If you want the entire NES.css UI styling system (buttons, containers, forms) bundled locally for offline availability:

1. Install the `nes.css` dependency in your Quartz project root:
   ```bash
   npm install nes.css
   ```

2. Reference the stylesheet from `node_modules` inside `quartz/styles/custom.scss` by omitting the `.css` extension to force Sass to inline the content:
   ```scss
   @import "nes.css/css/nes";
   ```

Esbuild's Sass loader will automatically resolve the package path, inline the framework rules, and compile them into your site's bundled `index.css`.

### Option 3: CDN Integration (Quickest Full Setup)

To load the full framework from a CDN with zero build-time impact, append the `@import` statement to the top of your `quartz/styles/custom.scss` file:

```scss
@import url("https://unpkg.com/nes.css@latest/css/nes.min.css");
```

---

## Core Styling Components

Once integrated, you can use any of the classes provided by NES.css within raw HTML blocks in your Obsidian Markdown notes.

### Containers

Create retro containers using `nes-container`:

```html
<div class="nes-container with-title is-centered">
  <p class="title">Retro Dashboard</p>
  <p>Welcome to the nostalgic zone.</p>
</div>
```

To create dark-themed boxes, add the `is-dark` class:

```html
<div class="nes-container is-dark with-title">
  <p class="title">System Log</p>
  <p>Status: Active</p>
</div>
```

### Buttons

NES.css offers several styled action buttons:

```html
<button type="button" class="nes-btn">Normal</button>
<button type="button" class="nes-btn is-primary">Primary</button>
<button type="button" class="nes-btn is-success">Success</button>
<button type="button" class="nes-btn is-warning">Warning</button>
<button type="button" class="nes-btn is-error">Error</button>
```

### Text Balloons

Perfect for retro dialogue bubbles:

```html
<div class="nes-balloon from-left">
  <p>Hello! I am a helper robot.</p>
</div>
```

### Retro Icons

NES.css includes highly detailed 8-bit sprites for icons, social media logos, and status indicators (like hearts and stars):

```html
<!-- Social Icons -->
<i class="nes-icon github"></i>
<i class="nes-icon twitter"></i>
<i class="nes-icon youtube"></i>

<!-- Status Icons -->
<i class="nes-icon heart"></i>
<i class="nes-icon star"></i>
<i class="nes-icon like"></i>
```

---

## Custom Theme Tuning

By default, Quartz has a set layout. If you want the pixelated aesthetic to apply smoothly to all components, you can add helper overrides to `quartz/styles/custom.scss`:

```scss
// Smooth pixel-art scaling for images and retro icons
img, .nes-icon {
  image-rendering: pixelated;
  image-rendering: crisp-edges;
}

// Hide the automatically appended external link icon for anchors wrapping a retro icon
a:has(.nes-icon) .external-icon {
  display: none;
}

// Retro border style for active elements
.nes-btn, .nes-container {
  font-family: var(--headerFont);
}
```

---

## Backstory & Philosophy

The creator, **B.C.Rikko**, developed NES.css as a way to overcome a personal dislike for CSS. By combining technical learning with a passion for retro aesthetics, they transformed a difficult skill into a creative project.

*   **Learning through Play:** The project served as a catalyst for learning modern CSS features (Flexbox, Box Model) in a fun, nostalgic context.
*   **Vibe Over Accuracy:** The philosophy prioritizes the "8-bit vibe" over strict historical accuracy (e.g., using a SNES controller icon despite the "NES" branding).
*   **Open Source Growth:** Released as Open Source to improve the tool and the author's own knowledge through community feedback.

---

## Connections
- [[Resources MOC]]
- [[Software Engineering MOC]]
- [[Jekyll MOC]]
