# Whatnotica - Site Migration Guide

This is the new Whatnotica website, built with [Zola](https://www.getzola.org/) static site generator and ready for free hosting on GitHub Pages.


#### Adding a New Product

1. Scan/photograph the artwork
2. Save the image to `static/images/` (e.g., `new-piece.jpg`)
3. Create a new file `content/products/new-piece.md`, copied from `PRODUCT_TEMPLATE.md` if you want:

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
Double-click on publish.sh, or:

```bash
git add -A
git commit -m "Add new piece: Name of the Piece"
git push
```

The site will auto-rebuild in ~1-2 minutes.

#### Removing a Product

Delete the markdown file and double-click on publish.sh, or:


```bash
rm content/products/old-piece.md
git add -A
git commit -m "Remove old-piece"
git push
```

