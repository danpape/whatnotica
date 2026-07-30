# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Whatnotica is a static website for an artist's hand-cut vintage paper collage gallery, built with **Zola** static site generator. The site was migrated from Shopify to reduce costs (~$420/year savings) and is designed to be hosted on GitHub Pages for free.

**Site**: https://www.whatnotica.com
**Stack**: Zola (static site generator) + GitHub Pages

## Essential Commands

### Development
```bash
# Install Zola (if not already installed)
sudo snap install zola

# Preview site locally (auto-reloads on changes)
zola serve
# Opens at http://127.0.0.1:1111

# Build production site (outputs to public/)
zola build

# Helper script that builds the site
./publish.sh
```

### Migration
```bash
# Scrape products from existing Shopify site
# Downloads images and generates markdown files
python3 scrape_shopify.py
```

## Important: Zola Version Compatibility

This site is configured for **Zola 0.22.1+**. The `config.toml` file has been updated to remove deprecated fields:
- Removed: `highlight_code` (no longer supported)
- Removed: `unsafe` from `[markdown]` section (no longer supported)

If working with older Zola documentation or templates, be aware that some configuration options have changed in newer versions.

## Architecture

### Content Model

**Products** are individual markdown files in `content/products/`. Each product file has:
- Frontmatter with `title`, `date`, and `extra` section containing `price` and `image` path
- Body containing the product description

Example product structure:
```markdown
+++
title = "Piece Name"
date = 2024-01-01

[extra]
price = "$7.00"
image = "images/filename.jpg"
+++

Description text here.
```

### Directory Structure

```
content/
├── _index.md                # Homepage (uses index.html template)
└── products/
    ├── _index.md            # Catalog section config (sorted by title)
    └── *.md                 # Individual product pages

templates/
├── base.html                # Main layout with header/footer/nav
├── index.html               # Homepage template (artist statement)
├── section.html             # Catalog grid view
└── page.html                # Individual product detail page

static/images/               # Product images (referenced as "images/filename.jpg")
sass/style.scss              # Site styles (compiled by Zola)
config.toml                  # Site configuration
```

### Template Hierarchy

1. **base.html**: Provides site-wide structure (header with nav, footer with contact)
2. **index.html**: Extends base, displays homepage with artist statement from `config.extra.artist_statement`
3. **section.html**: Extends base, shows product grid for `/products/` catalog
4. **page.html**: Extends base, displays individual product with image and purchase CTA

### Configuration (config.toml)

Important settings:
- `base_url`: Production domain
- `compile_sass = true`: Enables SCSS compilation
- `minify_html = true`: Minifies output
- `extra.contact_email`: Used in templates for purchase inquiries
- `extra.artist_statement`: Displayed on homepage

## Development Workflow

### Adding a New Product

1. Add image to `static/images/`
2. Create markdown file in `content/products/` with proper frontmatter
3. Preview with `zola serve`
4. Commit and push (auto-deploys via GitHub Actions)

### Removing a Product

1. Delete the markdown file from `content/products/`
2. Optionally remove the image from `static/images/`
3. Commit and push

### Editing Site Content

- Homepage artist statement: Edit `config.toml` → `extra.artist_statement`
- Contact email: Edit `config.toml` → `extra.contact_email`
- Styles: Edit `sass/style.scss` (auto-compiled by Zola)

## Deployment

Site auto-deploys to GitHub Pages via GitHub Actions workflow (see README.md for setup instructions). Workflow should:
1. Install Zola
2. Run `zola build`
3. Deploy `public/` directory to GitHub Pages

Custom domain `www.whatnotica.com` configured via DNS pointing to GitHub Pages.

## Migration Script (scrape_shopify.py)

The Python script fetches products from Shopify's JSON API (`/products.json` endpoint) and:
- Downloads product images to `static/images/`
- Generates markdown files in `content/products/`
- Uses `slugify()` to create URL-friendly filenames
- Strips HTML from Shopify descriptions

**Important**: When modifying the script, f-strings cannot contain backslashes in expressions. Pre-process any string replacements before using them in f-strings.

This is a one-time migration tool, not part of regular workflow.

## Important Notes

- Product images must be in `static/images/` and referenced in frontmatter as `images/filename.jpg` (relative to static/)
- The catalog (`content/products/_index.md`) is configured to sort products by title
- All product dates default to 2024-01-01 (used for sorting if needed)
- Site uses no JavaScript - pure HTML/CSS static generation
- Contact/purchase flow is email-based (mailto links)
