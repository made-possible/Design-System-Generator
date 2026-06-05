# GitHub Setup Guide — First Time

This walks you through creating a GitHub account, creating your repo, and uploading the Design System Maker files. Takes about 10 minutes.

---

## Part 1 — Create a GitHub account

1. Go to **[github.com](https://github.com)**
2. Click **Sign up** (top right)
3. Enter your email, create a password, choose a username
   - Pick something professional — it shows in all your repo URLs (e.g. `github.com/noahdijulio/design-system-maker`)
4. Verify your email address
5. On the "Welcome" screen, choose **Free** plan — it has everything you need

---

## Part 2 — Create the repository

A "repository" (repo) is just a folder on GitHub that holds your project files.

1. Once logged in, click the **+** icon (top right) → **New repository**
2. Fill in:
   - **Repository name:** `design-system-maker`
   - **Description:** `A Claude skill that audits any product and generates a complete design system — tokens, HTML reference site, and Figma export.`
   - **Visibility:** ✅ **Public** (required for free sharing)
   - **Initialize this repository with:**
     - ✅ Check **Add a README file** — uncheck this actually, since we have our own
     - Leave license as **None** for now (our README says MIT)
3. Click **Create repository**

---

## Part 3 — Upload your files

You'll see an empty repo page. Now upload the files:

1. Click **uploading an existing file** (the link in the middle of the page)
   - Or: click **Add file** → **Upload files**
2. Drag and drop all the files from your `design-system-maker` folder:
   - `SKILL.md`
   - `build_reference.py`
   - `build_figma.py`
   - `MASTER-SECTION-LIBRARY.md`
   - `DESIGN-SYSTEM-SPEC.md`
   - `README.md`
   - `design-system-maker.skill`
3. At the bottom, leave the commit message as-is ("Add files via upload") or type something like `Initial release`
4. Click **Commit changes**

Your repo is now live at `github.com/YOUR-USERNAME/design-system-maker` 🎉

---

## Part 4 — Create a Release (for the .skill download button)

The `.skill` file needs to be on the Releases page so people get a clean download link.

1. On your repo page, look at the right sidebar → click **Releases** → **Create a new release**
2. Click **Choose a tag** → type `v1.0` → click **Create new tag: v1.0**
3. **Release title:** `v1.0 — Initial Release`
4. **Description:** 
   ```
   First public release of Design System Maker.
   
   Download design-system-maker.skill below and drag it into Claude Cowork to install.
   ```
5. Under **Attach binaries**, drag in `design-system-maker.skill`
6. Click **Publish release**

Now your README's "Download from Releases" link will work.

---

## Part 5 — LinkedIn post tips

When you're ready to share:

- **Lead with a before/after** — a screenshot of a source website on the left, the generated HTML reference site on the right
- **Link:** `github.com/YOUR-USERNAME/design-system-maker`
- **CTA:** "Free download — drop the .skill file into Claude Cowork and it just works"
- **Tags:** #DesignSystems #Claude #AI #UX #DesignTokens #Figma

---

## Later: keeping files updated

When you improve the skill and want to push updates:

1. On your repo page, click on the file you want to update
2. Click the **pencil icon** (Edit this file)
3. Make your changes
4. Click **Commit changes**

Or for multiple files, use the **Add file → Upload files** route again — it will replace any file with the same name.

---

That's it! Questions? Ask Claude.
