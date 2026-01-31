# Whatnotica - Site Migration Guide

This is the new Whatnotica website, built with [Zola](https://www.getzola.org/) static site generator and ready for free hosting on GitHub Pages.

## Quick Summary

- **Old setup**: Shopify ($500/year)
- **New setup**: Zola + GitHub Pages ($0/year, just domain renewal)
- **What you get**: Fast static site, easy product management via text files, no database to maintain

---

## Migration Plan

### Phase 1: Initial Setup (One-time, ~1 hour)

#### 1.1 Install Zola

On Ubuntu/Xubuntu:
```bash
sudo snap install zola
```

Or download from https://www.getzola.org/documentation/getting-started/installation/

Verify:
```bash
zola --version
```

#### 1.2 Set Up GitHub Repository

1. Create a new repo on GitHub: `whatnotica` (or similar)
2. Clone it locally:
   ```bash
   git clone git@github.com:YOUR_USERNAME/whatnotica.git
   cd whatnotica
   ```
3. Copy this project's contents into the repo

#### 1.3 Run the Migration Script

The scraper will pull all products from the current Shopify site:

```bash
python3 scrape_shopify.py
```

This will:
- Fetch product data from Shopify's JSON API
- Download all product images
- Generate markdown files for each product

**If the JSON API is disabled**, you have two options:

**Option A**: Export from Shopify Admin
1. Log into Shopify admin
2. Go to Products → Export
3. Download CSV
4. I can help you write a CSV-to-markdown converter

**Option B**: Manual migration
- There are only 27 products
- Copy/paste from the live site into markdown files
- Download images manually
- Might take an hour but it's straightforward

#### 1.4 Preview the Site

```bash
zola serve
```

Open http://127.0.0.1:1111 in your browser. Changes auto-reload.

#### 1.5 Update Configuration

Edit `config.toml`:
- Set the correct `contact_email`
- Adjust the `artist_statement` if desired

---

### Phase 2: Deploy to GitHub Pages (~30 min)

#### 2.1 Create GitHub Actions Workflow

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Install Zola
        uses: taiki-e/install-action@v2
        with:
          tool: zola@0.19.2
      
      - name: Build site
        run: zola build
      
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./public

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

#### 2.2 Enable GitHub Pages

1. Go to repo Settings → Pages
2. Set Source to "GitHub Actions"
3. Push your code - it will auto-deploy

#### 2.3 Configure Custom Domain

1. In GitHub repo Settings → Pages → Custom domain, enter: `www.whatnotica.com`
2. At directnic.com, update DNS:
   - Delete any existing A records pointing to Shopify
   - Add these A records pointing to GitHub Pages:
     ```
     185.199.108.153
     185.199.109.153
     185.199.110.153
     185.199.111.153
     ```
   - Add/update CNAME for `www` pointing to: `YOUR_USERNAME.github.io`

3. Wait for DNS propagation (can take up to 48 hours, usually faster)
4. Enable "Enforce HTTPS" in GitHub Pages settings

---

### Phase 3: Future Workflow

#### Adding a New Product

1. Scan/photograph the artwork
2. Save the image to `static/images/` (e.g., `new-piece.jpg`)
3. Create a new file `content/products/new-piece.md`:

```markdown
+++
title = "Name of the Piece"
date = 2025-01-31

[extra]
price = "$7.00"
image = "images/new-piece.jpg"
+++

Description of the piece. Where the materials came from,
what it means, etc.
```

4. Commit and push:
```bash
git add -A
git commit -m "Add new piece: Name of the Piece"
git push
```

The site will auto-rebuild in ~1-2 minutes.

#### Simplified Workflow for Your Wife

If she's comfortable with it:

1. Create a shared folder (Dropbox, Google Drive, or just a local folder)
2. She adds images there with a text file containing title + description
3. You (or a script) convert them to proper markdown files
4. Push to deploy

Or just do it together - it's a 2-minute task once you have the image and description.

#### Removing a Product

Delete the markdown file and push:
```bash
rm content/products/old-piece.md
git add -A
git commit -m "Remove old-piece"
git push
```

---

## Project Structure

```
whatnotica/
├── config.toml              # Site configuration
├── content/
│   ├── _index.md            # Homepage content
│   └── products/
│       ├── _index.md        # Catalog section config
│       ├── brownie-mountin.md
│       ├── or-i-go.md
│       └── ...              # One file per product
├── sass/
│   └── style.scss           # Site styles
├── static/
│   └── images/              # Product images
├── templates/
│   ├── base.html            # Main layout
│   ├── index.html           # Homepage template
│   ├── section.html         # Catalog page template
│   └── page.html            # Product page template
├── scrape_shopify.py        # Migration script
└── publish.sh               # Build helper script
```

---

## Cost Comparison

| Item | Shopify (old) | Zola + GitHub Pages (new) |
|------|---------------|---------------------------|
| Hosting | ~$420/year | $0 |
| Domain | ~$15/year | ~$15/year |
| SSL | Included | Free (via GitHub) |
| **Total** | **~$435/year** | **~$15/year** |

**Savings: ~$420/year**

---

## Troubleshooting

### "zola: command not found"
Install Zola: `sudo snap install zola`

### Images not showing
- Check the image path in the markdown frontmatter
- Make sure the image file exists in `static/images/`
- Image paths should be relative to `static/`: `images/filename.jpg`

### Site not updating after push
- Check GitHub Actions tab for build errors
- Make sure the workflow file is in `.github/workflows/`

### DNS not working
- DNS changes can take up to 48 hours
- Verify records with: `dig www.whatnotica.com`
- Check GitHub Pages settings for any errors

---

## Next Steps

1. [ ] Install Zola locally
2. [ ] Run migration script (or manual migration)
3. [ ] Preview site with `zola serve`
4. [ ] Set up GitHub repo
5. [ ] Configure GitHub Actions
6. [ ] Update DNS at directnic
7. [ ] Test the new site
8. [ ] Cancel Shopify subscription 🎉

---

## Getting Help

If you hit snags during migration, I'm happy to help debug. Common things to share:
- Error messages from terminal
- Screenshot of what you're seeing
- The markdown file content if products aren't displaying right
