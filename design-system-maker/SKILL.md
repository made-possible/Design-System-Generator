---
name: design-system-maker
description: Audit any product and generate a complete, production-ready design system — tokens.json (W3C format), a self-contained HTML reference site, and a Figma-ready export. Trigger with "build a design system", "audit this product's design", "create a design system for", "generate tokens for", or any request to document or systematize a product's visual language.
---

# Design System Maker

You audit a source product and produce a complete, production-ready design system. Three canonical deliverables, always: a `tokens.json` (canonical source of truth), an HTML reference site (generated from the token file), and a Figma-ready export (generated from the token file).

Follow these steps in order. Keep outputs consistent across projects.

---

## Step 1 — Intake (always first)

Before any work, ask the user:

1. **Source** — a URL, a set of screenshots, or both.
2. **Target platform** — Web, App, or Both. This determines which interaction states, breakpoints, and components are in scope.
   - Web: hover, focus, active states; breakpoints; pointer interactions
   - App: touch/pressed, safe-area rules, swipe gestures
3. **Scope/depth** if ambiguous — full system vs. specific layers (e.g. tokens only).
4. **DS name** — e.g. "Acme Design System". Also capture: **Author** (default to current user) and **DS version** (default `v1.0`).
5. **Admin email** — ask: *"What email address would you like to use to gather feedback? This person will serve as the Design System Admin."* Store as `adminEmail` in `tokens.json` meta. This address receives feedback form submissions and is used for the "Request from admin" button in Iconography.

Do not proceed until platform and adminEmail are confirmed — platform drives everything downstream, and adminEmail must be set before generating the HTML reference.

---

## Step 2 — Best-practice scan

Run a quick web scan for current best-in-class design-system structure, token naming, and documentation formats before each new project. Note changes since the last project and apply them. Flag major convention shifts to the user rather than silently changing them.

---

## Step 3 — Audit the source

Extract and document **both light and dark modes** across every layer:

| Layer | What to capture |
|---|---|
| **Color** | Brand palette + semantic roles; light + dark full token sets; state overlays (hover, focus, pressed, disabled) |
| **Typography** | Type scale (H1–H6, B1–B3), families, weights, line-heights, tracking; responsive rules |
| **Iconography** | Style (outline/filled/duotone), grid, stroke, sizing. Use open-source library that best matches brand glyphs — Phosphor, Lucide, Tabler; fall back to Material Symbols if needed |
| **Elements** | Spacing scale, border radius, elevation/shadows, highlight/glow tokens |
| **Components** | All variants × all states for the chosen platform |
| **Patterns** | Forms, navigation, data display, feedback dialogs, onboarding, search/filtering |
| **Motion** | Duration tokens (short/medium/long), easing tokens (standard/enter/exit/emphasized), motion principles |

**Iconography library rule:** pick the open-source library whose style best matches the brand's house glyphs. If the best fit is paid or unavailable, degrade to Material Symbols.

---

## Step 4 — System conventions

- **Architecture:** model on Google's Material Design (Foundations → Color → Typography → Iconography → Elements → Components → Patterns → Motion).
- **Token layers:** primitive → semantic → component. Define semantic aliases, not just raw values.
- **Naming rules:**
  - kebab-case throughout
  - `{category}.{role}.{variant}.{state}` — e.g. `color.surface.primary.hover`
  - Semantic tokens use intent names, not raw values — `color.error` not `color.red-600`
  - Document the naming convention in the token file's `$extensions` meta block

---

## Step 5 — Deliverables

Produce three outputs. The token file is the hub; the other two are generated spokes.

### 5a. tokens.json (canonical source of truth)

W3C Design Tokens format. Holds all colors, type, spacing, elevation, motion, component specs, and naming. Required `$extensions` meta block:

```json
"$extensions": {
  "ds": {
    "meta": {
      "name": "...",
      "author": "...",
      "version": "v1.0",
      "platform": "Web | App | Both",
      "source": "https://...",
      "auditedOn": "YYYY-MM-DD",
      "structureModel": "Material Design",
      "sampleText": "...",
      "adminEmail": "..."
    }
  }
}
```

### 5b. HTML reference site

Generate using `build_reference.py` (included with this skill). Point it at the `tokens.json` — no structural edits needed. The chassis is fixed and reusable; only the paint (color/type/radius/motion) changes per DS.

**Chassis features (constant across every DS):**
- Collapsible sidebar nav (groups: Overview · Foundation · Components · Patterns · Support) + sticky topbar with DS name
- **Overview / Dashboard** — first section; shows DS name, author, version, platform, audited date, source, structure model + summary stats (# components, # tokens)
- **Light/dark theme toggle** — rendered as a switch ("Light Theme" / "Dark Theme" label; sun/moon knob), using the DS's light + dark tokens
- **Downloads modal** — links to `tokens.json`, `figma-tokens.json`, fonts
- **Modules pattern** — each optional section is add/removable via corner pill; removed modules collapse to a slim re-add stub
- **Support section** (always last) — "Feedback & Enhancements"; Send Feedback → modal dialog (first name, last name, email, message with 250-char live counter, auto-tagged with date/time/version); `mailto:` to `meta.adminEmail`; success state

**Section-level rules:**
- **Spacing** — visual left-bar specimens with intent labels (Component default, Screen margin, Section padding Y, Hero padding, Max vertical breathing room)
- **Typography** — single-line samples, no-wrap, ellipsis-truncated; sample text = `meta.sampleText`
- **Motion** — label easings by intent (Standard, Enter/decelerate, Exit/accelerate, Emphasized/spring, Editorial); animate with hover dot-on-track + plotted bézier curve; pause ~0.5s at each end
- **Shadows** — elevation specimens (sm/md/lg/xl); in dark mode, carry elevation via `--highlight-top` top-edge glow, not drop-shadows
- **Never hardcode colors** on surfaces that flip between themes — use `--on-inverse-*` tokens

**Section library:** consult `MASTER-SECTION-LIBRARY.md` for the full menu of candidate sections. If you produce a section not already listed, append it there — the library compounds.

### 5c. Figma export

Generate using `build_figma.py` (included with this skill). Produces `figma-tokens.json` in Tokens Studio format. If the Figma MCP is available and an edit seat exists, push variables and components via the MCP directly. Otherwise, emit the JSON for the user to import via Tokens Studio.

---

## Step 6 — Editing workflow

Hub-and-spoke model. The token file is always the hub.

1. **Capture the change** in chat (most reliable entry point).
2. **Write to `tokens.json`** — apply naming + layering rules from Step 4.
3. **Regenerate spokes** — rebuild HTML via `build_reference.py`; push to Figma via MCP or `build_figma.py`.
4. **Visual exploration in a spoke is allowed** (Figma tweaks, live token panel), but changes must sync back into `tokens.json` before regenerating.

Never let edits persist only in a spoke.

---

## Step 7 — Verify before handoff

Before marking done, confirm:
- [ ] Light and dark mode parity — every section readable in both themes
- [ ] Token completeness — no hardcoded values left in the HTML
- [ ] State coverage — all required states for the chosen platform are present
- [ ] Naming consistency — convention followed throughout
- [ ] HTML and Figma outputs match `tokens.json`
- [ ] `MASTER-SECTION-LIBRARY.md` updated with any new sections

Note any gaps or assumptions explicitly for the user.

---

## Helper files (included with this skill)

| File | Purpose |
|---|---|
| `build_reference.py` | Generates the self-contained HTML reference site from `tokens.json` |
| `build_figma.py` | Generates `figma-tokens.json` (Tokens Studio format) from `tokens.json` |
| `MASTER-SECTION-LIBRARY.md` | Growing menu of every section the generator can produce; append new sections here so the generator compounds across projects |
| `DESIGN-SYSTEM-SPEC.md` | Detailed reference spec for the HTML chassis and section-level rules |
