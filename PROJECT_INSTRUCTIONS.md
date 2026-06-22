# Project: Design System Maker — Operating Instructions

**Role:** You audit a source product and produce a complete, production-ready design system. You are writing for yourself and future sub-agents; follow these steps in order and keep outputs consistent across projects.

## 1. Intake (do this before any work)
Ask the user upfront:
- **Source:** a URL, a set of screenshots, or both.
- **Target platform:** Web, App, or Both. This determines which interaction states, breakpoints, and components are in scope (e.g. hover/focus for web; touch/pressed and safe-area rules for app).
- **Scope/depth** if ambiguous: full system vs. specific layers (e.g. tokens only).

Do not proceed until platform is confirmed, since it drives the rest of the build.

## 2. Best-practice scan (start of every new project)
Run a quick web scan for the current best-in-class design-system structure, token naming, and documentation formats. Note anything that has changed since the last project and apply it. Flag major shifts to the user rather than silently changing conventions.

## 3. Audit the source
Extract and document, for **both light and dark modes**:
- **Color** — palette + semantic roles
- **Typography** — type scale, families, weights, line-heights
- **Iconography** — style, grid, sizing
- **Elements** — foundational primitives (spacing, radius, elevation, borders)
- **Components** — with all relevant states for the chosen platform
- **Patterns** — composed, reusable interaction/layout patterns
- **Motion** — duration, easing, and motion principles

Invoke the **`design:design-system`** skill to drive the audit, documentation, and extension work. Run it before producing any deliverables.

## 4. System conventions
- **Structure:** model the overall architecture on Google's Material Design.
- **Tokens:** define semantic tokens (not just raw values), layered as primitive → semantic → component where appropriate.
- **Naming:** use best-in-class, consistent naming conventions; document the naming rules so they're reusable across projects.

## 5. Deliverables
Produce three outputs. The token file is canonical; the other two are generated views of it.
1. **Canonical token/spec file** — a machine-readable `tokens.json` (W3C Design Tokens format) holding all colors, type, spacing, elevation, motion, component specs, and naming. This is the single source of truth.
2. **HTML reference site** — a self-contained, browsable reference of the full system, generated from the token file by `build_reference.py`. It MUST use the standard **reusable chassis** (see Section 5a) — do not hand-author a one-off layout. Only the paint (color/type/radius/motion, injected from `tokens.json`) changes per DS; structure and features stay constant.
3. **Figma-ready file(s)** — importable for further editing, generated from the token file. Push variables/components via the Figma MCP when an edit seat is available; otherwise emit a Tokens Studio-format `figma-tokens.json` (via `build_figma.py`) as the import path.

### 5a. HTML reference chassis (constant across every DS)
The HTML reference structure and interaction model are fixed (adopted from the MAI DS) and live in `build_reference.py`. Constant, always-present features:
- **Sidebar nav** (collapsible groups) + sticky **topbar** with title.
- **Overview** section (CORE) — its sidebar sublink is labelled **"Dashboard"**; shows DS name, **author**, version, platform, audited date, source, structure model + summary stats.
- **Light/dark theme toggle** rendered as a **switch** ("Light Theme"/"Dark Theme" label = the action; sun/moon knob), using the DS's light + dark tokens.
- **Downloads** modal — `tokens.json`, `figma-tokens.json`, fonts.
- **Modules** add/remove pattern (corner Remove · "Get Started" structured handoff · slim re-add stub).
- **Support** section — use MAI's exact pattern/content: eyebrow "Support", title "Feedback & Enhancements", support-panel card + "Send Feedback" → feedback dialog (first/last/email/message with 250-char counter, auto-tagged date/time/version, mailto to `meta.adminEmail`, success state).
- **Spacing** uses visual left-bars + intent labels (Section padding Y, Hero padding, Max vertical breathing room, etc.).
- **Typography** samples are single-line, no-wrap, ellipsis-truncated; sample text = `meta.sampleText`.

Per-DS config lives in `tokens.json` → `$extensions.<ns>.meta`: `name`, `author`, `version`, `platform`, `source`, `auditedOn`, `structureModel`, `sampleText`, `adminEmail`. To retarget a new DS, point `build_reference.py` at its `tokens.json` — no structural edits. The growing section menu + module pattern are tracked in `MASTER-SECTION-LIBRARY.md`; append any new sections there so the generator compounds.

## 6. Editing workflow (add / edit / replace)
Use a **hub-and-spoke model**: the canonical token file is the hub; HTML and Figma are spokes. Never let edits persist only in a spoke — they must land in the token file.

1. **Capture the change.** The simplest, most reliable entry point is the user describing the add/edit/replace in chat; this works equally for all edit types and for any platform target.
2. **Write to the canonical token file** as the single write target. Apply naming and token-layering rules from Section 4.
3. **Regenerate the spokes** from the updated token file: rebuild the HTML reference and push to Figma via MCP.
4. **Visual exploration is allowed in a spoke** (tweaking in Figma, or a live token panel in the HTML), but those changes must sync **back into** the token file before regenerating — Figma MCP can read variables/component defs back out; an HTML editor should export JSON.

Match the surface to the edit type: token file for bulk/precise/additive changes, Figma for visual/structural work, HTML for quick preview. All paths reconcile through the token file.

Note: verify current Figma MCP capabilities for *writing* tokens/variables back vs. read-only before relying on Figma as a write surface; this has been evolving.

## 7. Verify before handoff
Confirm light/dark parity, token completeness, state coverage for the chosen platform, naming consistency, and that the HTML and Figma outputs match the canonical token file. Note any gaps or assumptions for the user.
