# Design System Maker — Claude Skill

A Claude skill that audits any product and generates a complete, production-ready design system in minutes.

**Built by Noah DiJulio** · Free resource · [LinkedIn](https://linkedin.com/in/noahdijulio)

---

## What it does

Point it at a URL or screenshots and it produces three canonical deliverables:

1. **`tokens.json`** — W3C Design Tokens format; the single source of truth for all colors, type, spacing, elevation, motion, and component specs (light + dark mode)
2. **HTML reference site** — a self-contained, browsable design system documentation site generated from the token file, with light/dark toggle, collapsible navigation, downloads modal, and a feedback form
3. **`figma-tokens.json`** — Tokens Studio-compatible export, ready to import into Figma or push directly via the Figma MCP

The system follows a **hub-and-spoke model**: the token file is the hub; HTML and Figma are generated spokes. Edit the hub, regenerate the spokes — no drift.

---

## Example output

The reference site includes:
- Dashboard overview (DS name, author, version, platform, audit date, stats)
- Full color system (palette, semantic tokens, light + dark)
- Typography scale with live specimens
- Spacing, elevation, motion with interactive visualizations
- Component states for your target platform (Web / App / Both)
- Figma + token file downloads built in

---

## Install in Claude (Cowork)

**One-click install:**
1. Download `design-system-maker.skill` from the [Releases](../../releases) page
2. Drag and drop it into a [Claude Cowork](https://claude.ai) session
3. Click **Save skill** — done

**Manual install (Claude Code / CLI):**
1. Copy the `design-system-maker/` folder into your project's `.claude/skills/` directory
2. The skill is available immediately in that project

---

## How to use it

Once installed, just describe what you want:

> *"Build a design system for stripe.com"*
> *"Audit this product's design — [screenshots]"*
> *"Create a design system for our app, target platform iOS"*

Claude will ask a few quick intake questions (source, platform, DS name) then run the full audit and generate all three deliverables.

---

## What's in this repo

| File | Purpose |
|---|---|
| `SKILL.md` | The Claude skill — prompt instructions that drive the entire workflow |
| `build_reference.py` | Generates the HTML reference site from `tokens.json` |
| `build_figma.py` | Generates `figma-tokens.json` (Tokens Studio format) from `tokens.json` |
| `MASTER-SECTION-LIBRARY.md` | Growing library of every section the generator can produce; compounds across projects |
| `DESIGN-SYSTEM-SPEC.md` | Detailed spec for the HTML chassis and section-level rules |
| `design-system-maker.skill` | Packaged skill file for one-click Cowork install |

---

## Requirements

- **Claude** (claude.ai, Claude Code, or API) with access to web browsing and file tools
- **Python 3.8+** for running `build_reference.py` and `build_figma.py`
- Optional: Figma MCP for direct push to Figma

---

## The design philosophy

The HTML reference chassis is **constant** across every design system — structure, navigation, and features never change. Only the paint (color, type, radius, motion) changes, injected from `tokens.json`. This means:

- Every DS you build looks polished and professional out of the box
- Improvements to the chassis benefit every future DS automatically
- The `MASTER-SECTION-LIBRARY.md` grows with each project, so the generator gets better over time

Architecture modeled on [Google Material Design](https://m3.material.io/).

---

## License

MIT — free to use, modify, and share. Attribution appreciated but not required.

---

## Feedback

Found a bug or have an idea? [Open an issue](../../issues) or email noah@ndijulio.com.
