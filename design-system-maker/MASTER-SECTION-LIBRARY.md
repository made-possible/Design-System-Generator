# Design System — Master Section Library

> **Purpose:** A growing master list of every section and subsection the design-system
> generator can produce. The intent is a best-in-class generator that improves over time:
> each new project appends any *new* section/subsection it invents here, so future
> projects inherit it. Structure mirrors Material Design (Google).
>
> **How to use**
> 1. When auditing/building, treat this as the menu of candidate sections.
> 2. If a project produces a section/subsection not already listed, **add it here** with a
>    one-line description so the library compounds.
> 3. Per project, mark each section: `core` (always include), `optional`, or `module`
>    (a self-contained, addable/removable block — see "Module Pattern" below).

---

## 1. Foundations
- **Design principles** — guiding values, voice, brand personality
- **Platform scope** — Web / App / Both (drives required states & breakpoints)
- **Grid & layout** — columns, gutters, margins, breakpoints, responsive rules
- **Spacing scale** — base unit, scale steps, component padding/inset
- **Elevation** — light & dark levels, shadow tokens, surface tints
- **Accessibility baseline** — WCAG target, contrast minimums, focus visibility, touch targets

## 2. Color
- **Brand palette** — primary, secondary, tertiary, ramps
- **Neutral palette** — greys, surfaces, backgrounds
- **Semantic colors** — success, warning, error, info
- **Semantic tokens** — role-based aliases (`color.surface`, `color.on-surface`)
- **Light mode** — full token set
- **Dark mode** — full token set, elevation overlays
- **State colors** — hover, pressed, focus, selected, disabled overlays

## 3. Typography
- **Type scale** — display, headline, title, body, label tiers
- **Font families** — primary, secondary, mono
- **Weights & styles** — weight ramp, italics
- **Line height & tracking** — per scale step
- **Responsive type** — fluid scaling rules
- **Typography tokens** — semantic aliases

## 4. Iconography
- **Icon style** — outline/filled/duotone, grid, stroke
- **Sizing & spacing** — size ramp, optical alignment
- **Usage guidelines** — pairing with text, color application
- **Icon tokens** — named sizes/colors

## 5. Elements (atoms)
- **Buttons** — variants, sizes, states
- **Inputs & fields** — text, select, checkbox, radio, switch, slider
- **Chips / tags / badges**
- **Avatars**
- **Links**
- **Dividers**
- **Loaders / progress / skeletons**

## 6. Components (molecules / organisms)
- **Variants** — primary, secondary, ghost, etc.
- **States** — default, hover, active, focus, disabled, loading, error, selected
- **Sizes** — sm / md / lg
- **Anatomy** — labeled parts
- **Props / API**
- **Behavior** — interactions, animations
- **Accessibility** — ARIA, keyboard, screen reader
- **Do's & Don'ts**
- **Code example**

## 7. Patterns
- **Forms** — input groups, validation, submission, error recovery
- **Navigation** — sidebar, tabs, breadcrumbs, app bar, bottom nav (App)
- **Data display** — tables, cards, lists, empty states
- **Feedback** — toasts, modals, dialogs, inline messages, banners
- **Onboarding & empty states**
- **Search & filtering**

## 8. Motion
- **Duration tokens** — short / medium / long
- **Easing tokens** — standard, decelerate, accelerate, emphasized
- **Motion principles** — purpose, choreography, reduced-motion
- **Transition patterns** — enter/exit, shared element, state change

## 9. Naming & Tokens
- **Token architecture** — primitive → semantic → component tiers
- **Naming conventions** — casing, namespacing, structure
- **Token reference table**

## 10. Modules (Add-on Systems)
- **Add-on systems / section packs** — optional design systems presented as addable/
  removable modules (e.g. Marketing Site Kit, Data Visualization Pack).
- Uses the **Module Pattern** below: corner Remove, "Get Started" setup flow, slim re-add stub.

## 11. Feedback & Enhancements
- Captured improvement ideas, open questions, proposed additions to the system.
- This is the visual template for the **Module Pattern** below.

---

## Module Pattern (Add / Remove)

When a *new* design system (or a new optional section) is generated, present it as a
**module** in the HTML reference, styled exactly like the "Feedback & Enhancements"
section (the canonical template). Anatomy, top to bottom:

1. **Eyebrow** — small uppercase, letter-spaced category label (e.g. `SUPPORT`, `MODULE`).
2. **Title** — large serif italic heading (the module / design-system name).
3. **Card** — soft-bordered, tinted-surface rounded card containing, centered:
   - a circular outlined **icon** badge,
   - a serif italic **sub-heading**,
   - one or two lines of muted **description** copy,
   - a single **pill action button**.

### Control model (confirmed with Noah — current standard)
- **Remove** lives in the **upper-right corner of the card** (a small outlined pill),
  mirroring the position of the stub's **Add** button.
- The card's **centered primary action is "Get Started"**, not Add. Get Started opens the
  module setup/configuration flow (see below). Add only appears on the slim stub.
- **Remove** = *hide + mark excluded*: the module is hidden from the active view AND
  flagged `data-included="false"` so it is excluded from the active system/export. The
  definition is **kept in the library** and is re-addable.
- A removed module collapses to a **slim re-add stub** — a thin dashed bar showing the
  module name + an upper-right **Add** button — so it's easy to bring back. It never
  fully disappears.

### Module creation flow — "Get Started" (structured handoff — chosen standard)
The recommended path for authoring a new module is a **structured handoff**, not an
in-browser builder (too brittle, duplicates logic) and not a freeform Claude prompt
(loses structure). "Get Started" stays in the browser only to *capture intent*, then
emits a ready-to-paste prompt that Claude uses to author the module.

1. Get Started opens a short dialog: **platform** picker (Web / App / Both) + optional
   **special requirements** notes. Marks the module `data-included="true"`.
2. It generates a **scoped prompt** referencing the module name + scope, platform, notes,
   the target HTML file, and an instruction to inherit existing tokens and to **append the
   module to `MASTER-SECTION-LIBRARY.md`** (Change Log + relevant section).
3. User copies the prompt into this Claude project; Claude builds the module and grows the
   library — so the generator compounds each time.

**End-state (future):** once the Figma MCP + file-write loop is wired, Get Started can call
Claude directly to author the module into the HTML and push matching Figma components —
removing the copy-paste. The captured config (platform, notes, scope) is exactly what that
MCP call needs.

Reference markup for the HTML output:

```html
<!-- Active module: full card, pill = Remove -->
<section class="ds-module" data-module="[name]" data-included="true">
  <p class="ds-module__eyebrow">MODULE</p>
  <h2 class="ds-module__title">[Module name]</h2>
  <div class="ds-module__card">
    <span class="ds-module__icon"><!-- outlined icon --></span>
    <h3 class="ds-module__subhead">[Sub-heading]</h3>
    <p class="ds-module__desc">[One or two lines of description.]</p>
    <button class="pill" data-action="remove">Remove</button>
  </div>

  <!-- Slim re-add stub, shown only when excluded -->
  <div class="ds-module__stub">
    <span>[Module name]</span>
    <button class="pill pill--ghost" data-action="add">Add</button>
  </div>
</section>
```

```js
document.querySelectorAll('.ds-module').forEach(m => {
  const set = on => {
    m.dataset.included = on ? 'true' : 'false';   // drives export inclusion
    m.classList.toggle('is-excluded', !on);       // CSS swaps card <-> stub
  };
  m.querySelector('[data-action="remove"]').onclick = () => set(false);
  m.querySelector('[data-action="add"]')   .onclick = () => set(true);
});
```

```css
/* When excluded: hide the full card, reveal the slim stub */
.ds-module .ds-module__stub { display: none; }
.ds-module.is-excluded .ds-module__card { display: none; }
.ds-module.is-excluded .ds-module__stub { display: flex; align-items: center; justify-content: space-between; }
/* Export/generation step should skip any [data-included="false"] module. */
```

---

## Change Log
> Append new sections/subsections discovered in future projects here.

| Date | Project | New section/subsection added |
|------|---------|------------------------------|
| 2026-06-04 | (initial) | Library seeded from Material-style taxonomy + Module Pattern |
| 2026-06-04 | MAI | Added §10 Modules (Add-on Systems); corner Remove + "Get Started" structured-handoff flow set as standard |
| 2026-06-05 | Wise | HTML reference CHASSIS standardized (from MAI): reusable, token-driven shell that is constant across every DS — only paint (color/type/radius/motion from tokens.json) changes. Generated by `build_reference.py`. Constant features: collapsible **sidebar nav** + sticky **topbar**, **light/dark theme toggle**, **Downloads** modal (tokens.json, figma-tokens.json, fonts), **Modules** add/remove pattern, **Support** section. **Overview** section is now CORE for every DS (DS name, author, version, platform, audited date, source, structure model + summary stats). Token→CSS-var mapping in `theme_vars()`; nav order in `NAV` registry. |
| 2026-06-05 | Wise | Chassis refinements set as standard for all future DSs: (1) **Spacing** uses MAI visual left-bars (`.space-row`/`.space-bar`) + intent labels via `SPACE_INTENT` (Component default, Screen margin, Section padding Y, Hero padding, Max vertical breathing room). (2) **Typography** samples are single-line, no-wrap, ellipsis-truncated; sample text = `meta.sampleText` (Wise: "One account, all kinds of money") — no DS-name prefix. (3) Theme control is a **switch** ("Light Theme"/"Dark Theme" label = action; sun/moon knob). (4) Overview sidebar sublink labelled **"Dashboard"**. (5) **Support** uses MAI's exact pattern/content — eyebrow "Support", title "Feedback & Enhancements", support-panel card + "Send Feedback" → feedback dialog (first/last/email/message 250-char counter, auto-tagged date/time/version, mailto to `meta.adminEmail`, success state). New meta fields: `sampleText`, `adminEmail`. |
