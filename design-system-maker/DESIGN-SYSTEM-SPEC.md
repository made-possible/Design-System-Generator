# Design System Maker — Required Reference-Site Structure

Apply this to **every** design system (DS) created in this project. The working reference
implementation is `microsoft-ai-design-system.html` — mirror its markup, token usage, and JS.

> **Skill to use:** Invoke the `design:design-system` skill (Audit, document, or extend a
> design system) before producing the HTML reference and Figma-ready files for any audit.

## 0. Name the design system first
At the start of every new DS creation, ask the user to **name the design system**
(e.g. "MAI Design System"). Also capture:
- **Author** — default to the current user.
- **DS version** — default `v1.0`.
- Refer to the owner as the **Design System Admin** (not "maintainer").

Use the name in the page title, sidebar logo, and dashboard byline.

## 1. Left column navigation (sidebar)
- Persistent left sidebar listing every section, grouped under labels:
  **Overview · Foundation · Components · Patterns · Support** (add more as needed).
- Each group is a **collapsible / expandable accordion**: the group label is a `<button>`
  that toggles a `.collapsed` class, with `aria-expanded` and a rotating caret/chevron.
  Sub-section links sit in a `.ds-nav-list` body that animates open/closed.
- **Group labels** carry a meaningful, distinct icon.
- **Sub-section links** use a single uniform marker (a `+`), NOT distinct per-item icons —
  per-item icons compete with and duplicate the group icon.
- **Default icon library: Phosphor** (`<script src="https://unpkg.com/@phosphor-icons/web"></script>`).
- Active-section highlighting on scroll via IntersectionObserver.

## 2. Overview / Dashboard section (first section, `#dashboard`)
Title: **"Dashboard"**. Includes:
- **Created by** (author) + DS version, shown with avatar/byline.
- Metric cards: **# Components**, **# Tokens**, **# Active Users** (real counts where possible).
- **# Teams** and **# Support Tickets** as cards marked **"Soon"** / future release (value `—`).
- A note clarifying which metrics are illustrative placeholders vs. real counts.

## 3. Foundation sections

### Typography
- Document a **named scale**: **H1–H6** for headings and **B1–B3** for body, each shown as a
  specimen with full spec (size / weight / line-height / tracking / family / usage).
- Add a **"Download fonts"** button in the top header (and in the typography section). It opens a
  dialog listing only **custom** font families with a Free (download) or Paid (purchase at foundry)
  source link. **Skip preinstalled system defaults** (Georgia, system sans/mono) — if all faces are
  system defaults, show a "nothing to download" state.

### Iconography
- Show the **icon source** label and license (e.g. "Phosphor — open source").
- **Library selection rule:** always pick the open-source library whose style best matches the
  brand's house glyphs (Phosphor, Lucide, Tabler, etc.). If the best fit is **paid or unavailable,
  degrade to Material Symbols** as the open-source default.
- Provide a **Download set** button (link to the library) and, for any custom/in-house glyphs, a
  **Request from admin** button (mailto to the author).

### Shadows & Highlights
- **Shadows** = elevation specimens (sm/md/lg/xl).
- **Highlights/Glows are the inverse of shadows.** In light mode depth reads as a cast shadow below;
  in **dark mode** cast shadows disappear, so elevation is carried by a faint **top-edge highlight**.
  Provide `--highlight-top` (elevation), `--highlight-focus` (focus ring), `--highlight-accent`
  (emphasis glow). Glows are for focus/accent emphasis, not general light-mode elevation.
- If a system genuinely has no highlight styles, show a **zero state** prompting to add them.

## 4. Motion
- Relabel easings **by intent** (Standard, Enter/decelerate, Exit/accelerate, Emphasized/spring, Editorial).
- Visualize each easing with a **hover dot-on-track + plotted bézier curve**. The dot travels the
  track using that curve and **pauses ~0.5s at each end** (hold at the extremes of the keyframes).
- Keep each easing spec on **one line** (intent + token, no wrapping).

## 5. Support / Feedback section (last section, `#support`)
- Copy: **"To submit feedback or feature enhancements, email us."**
- Primary CTA opens a **modal `<dialog>` feedback form** capturing first name, last name, sender
  email, and an open feedback field **capped at 250 characters** with a live counter.
- On submit, build a `mailto:` to the **author (Design System Admin)** with the body **auto-tagged
  with date, time, and DS version**, then show confirmation.
- Note: `mailto:` opens the user's mail client; true silent submission needs a form endpoint/connector.

## 6. Dark mode / theming rules
- **Never hardcode colors on a surface that itself flips between themes.** Any inverse/dark block
  (footer, dark CTA sections) must use dedicated flipping **"on-inverse" tokens** (e.g.
  `--on-inverse-link`, `--on-inverse-muted`, `--on-inverse-subtle`, `--on-inverse-faint`,
  `--on-inverse-border`, `--on-inverse-hover`) so text/borders stay legible in both light and dark.
- Verify both themes before sign-off — toggle dark mode and confirm every section, especially
  inverse blocks, remains readable.

## Tidy-ness rules
- Token tables should scan cleanly: stack full-width and prevent cell text from wrapping/stacking.
- Single-action dialogs use one button (e.g. **OK**) — no redundant close "×" plus button.

Reference implementation: `microsoft-ai-design-system.html` in this project.
