#!/usr/bin/env python3
"""Generate the HTML reference site from the canonical tokens.json.

REUSABLE CHASSIS: the structure, interaction model and feature set are constant
across every design system (adopted from the MAI HTML DS) -- sidebar nav, sticky
topbar, light/dark theme toggle, downloads, Overview, Modules (add/remove) and
Support. Only the PAINT changes per DS: all colour, typography, radius and motion
are injected from tokens.json. To retarget to a new DS, point this at that DS's
tokens.json (with $extensions.<ns>.meta) -- no structural edits needed.

Run: python3 build_reference.py
"""
import json, html, pathlib

ROOT = pathlib.Path(__file__).parent
tokens = json.load(open(ROOT / "tokens.json"))
esc = html.escape

# ---- meta (namespace-agnostic: first *.meta under $extensions) ----
meta = {}
for k, v in tokens.get("$extensions", {}).items():
    if k.endswith(".meta"):
        meta = v; break
DS_NAME  = meta.get("name", "Design System")
VERSION  = meta.get("version", "1.0")
AUTHOR   = meta.get("author", "—")
SOURCE   = meta.get("source", "")
AUDITED  = meta.get("auditedOn", "")
PLATFORM = meta.get("platform", "web")
ADMIN_EMAIL = meta.get("adminEmail", "")
SAMPLE   = meta.get("sampleText", DS_NAME)

P, S, C = tokens["primitive"], tokens["semantic"], tokens["component"]

def resolve(ref, root=tokens):
    if not (isinstance(ref, str) and ref.startswith("{") and ref.endswith("}")):
        return ref
    node = root
    for p in ref[1:-1].split("."):
        node = node[p]
    v = node["$value"]
    return resolve(v, root) if isinstance(v, str) and v.startswith("{") else v

def derived(n): return bool(n.get("$extensions", {}).get("wise.derived"))
def rv(d, *path):
    n = d
    for p in path: n = n[p]
    return resolve(n["$value"])

# ============================================================
# PAINT: map this DS's semantic tokens -> chassis CSS variables
# ============================================================
def theme_vars(theme):
    c = S["color"][theme]
    g = lambda *p: resolve(c[p[0]][p[1]]["$value"])
    return {
        "--surface-page":      g("background","screen"),
        "--surface-elevated":  g("background","elevated"),
        "--surface-subtle":    g("background","neutral"),
        "--border-default":    g("border","neutral"),
        "--text-primary":      g("content","primary"),
        "--text-secondary":    g("content","secondary"),
        "--text-tertiary":     g("content","tertiary"),
        "--text-link":         g("content","link"),
        "--interactive-bg":    g("interactive","primary"),
        "--interactive-text":  g("interactive","contrast"),
        "--accent-bg":         g("interactive","accent"),
        "--accent-text":       g("interactive","control"),
        "--sentiment-pos":     g("sentiment","positive"),
        "--sentiment-neg":     g("sentiment","negative"),
        "--sentiment-warn":    g("sentiment","warning"),
        "--focus-ring":        g("interactive","primary"),
    }

font_body    = (resolve(S["typography"]["family"]["default"]["$value"]) or ["Inter"])
font_display = (resolve(S["typography"]["family"]["display"]["$value"]) or ["Inter"])
FONT_BODY    = font_body[0] if isinstance(font_body, list) else font_body
FONT_DISPLAY = font_display[0] if isinstance(font_display, list) else font_display

radius_card = rv(S["radius"], "medium")
radius_pill = "999px"

def vars_block(selector, d):
    body = "".join(f"    {k}: {v};\n" for k, v in d.items())
    return f"  {selector} {{\n{body}  }}\n"

light = theme_vars("light")
dark  = theme_vars("dark")
light.update({"--font-body": f"'{FONT_BODY}', system-ui, sans-serif",
              "--font-display": f"'{FONT_DISPLAY}', '{FONT_BODY}', sans-serif",
              "--radius-card": radius_card, "--radius-pill": radius_pill})
NL = "\n"
light_css = "".join(f"  {k}:{v};{NL}" for k, v in light.items())

# ============================================================
# CONTENT renderers (generic over the token tree)
# ============================================================
def swatches(group):
    out = ""
    for name, node in group.items():
        if name.startswith("$"): continue
        val = resolve(node["$value"]); d = node.get("$description","")
        tag = '<span class="d">derived</span>' if derived(node) else ""
        out += (f'<div class="sw"><span class="chip" style="background:{val}"></span>'
                f'<div><code>{esc(name)}</code>{tag}<span class="v">{esc(str(val))}</span>'
                f'<p>{esc(d)}</p></div></div>')
    return f'<div class="sw-grid">{out}</div>'

def color_theme(theme):
    g = S["color"][theme]; out = ""
    for cat in ["content","interactive","background","border","sentiment","base"]:
        if cat in g:
            out += f'<h4>{cat.title()}</h4>{swatches(g[cat])}'
    return out

def dim_table(group, label="Token"):
    rows = ""
    for name, node in group.items():
        if name.startswith("$") or not isinstance(node, dict) or "$value" not in node: continue
        rows += (f'<tr><td><code>{esc(name)}</code></td><td>{esc(str(resolve(node["$value"])))}</td>'
                 f'<td>{esc(node.get("$description",""))}</td></tr>')
    return (f'<table><thead><tr><th>{label}</th><th>Value</th><th>Notes</th></tr></thead>'
            f'<tbody>{rows}</tbody></table>')

def type_rows():
    out = ""
    for name, node in S["typography"]["style"].items():
        if name.startswith("$"): continue
        v = node["$value"]; fam = resolve(v["fontFamily"])
        famn = fam[0] if isinstance(fam, list) else fam
        out += (f'<div class="typerow"><div class="sample" style="font-family:\'{famn}\',sans-serif;'
                f'font-weight:{v.get("fontWeight",500)};font-size:{v["fontSize"]};line-height:{v["lineHeight"]}">'
                f'{esc(SAMPLE)}</div>'
                f'<div class="meta"><code>{esc(name)}</code> <span class="d">derived</span><br>'
                f'{esc(famn)} · {v["fontSize"]}/{v["lineHeight"]} · {v.get("fontWeight",500)}</div></div>')
    return out

# Intent labels for the spacing scale (px value -> human intent). Constant across DSs.
SPACE_INTENT = {
    "16px": "Component default",
    "24px": "Screen margin (mobile)",
    "32px": "Section padding Y · between sections",
    "64px": "Hero padding",
    "80px": "Hero padding (large)",
    "128px": "Max vertical breathing room",
}
def space_bars():
    rows = ""
    for name, node in P["dimension"].items():
        if name.startswith("$"): continue
        val = resolve(node["$value"])
        try: px = int(str(val).replace("px",""))
        except ValueError: px = 0
        if px == 0: continue
        intent = SPACE_INTENT.get(val, "")
        intent_html = f' · <span class="space-intent">{esc(intent)}</span>' if intent else ""
        rows += (f'<div class="space-row"><div class="space-bar" style="width:{px}px"></div>'
                 f'<div class="space-info">{esc(name)} · {esc(str(val))}{intent_html}</div></div>')
    return rows

def radii_demo():
    out = ""
    for k, n in P["radius"]["desktop"].items():
        if k.startswith("$"): continue
        val = resolve(n["$value"])
        out += f'<div style="border-radius:{val}">{k}<br>{val}</div>'
    return f'<div class="radii">{out}</div>'

def grid_table():
    bps = S["grid"]["$extensions"]["wise.breakpoints"]; rows = ""
    for k, v in bps.items():
        rows += (f'<tr><td>{k.upper()}</td><td>{v.get("range","")}</td><td>{v.get("columns","")}</td>'
                 f'<td>{v.get("margin", v.get("behaviour",""))}</td><td>{v.get("gutter","")}</td></tr>')
    return (f'<table><thead><tr><th>BP</th><th>Range</th><th>Cols</th><th>Margin</th><th>Gutter</th>'
            f'</tr></thead><tbody>{rows}</tbody></table>')

def button_demo():
    rad = rv(C["button"], "radius")
    defs = [("Primary","--accent-bg","--accent-text"),
            ("Secondary","--interactive-bg","--interactive-text"),
            ("Secondary neutral","--surface-subtle","--text-link"),
            ("Tertiary","transparent","--text-link"),
            ("Negative","--sentiment-neg","#fff")]
    out = ""
    for label, bg, fg in defs:
        bgv = bg if bg=="transparent" else f"var({bg})"
        fgv = fg if fg.startswith("#") else f"var({fg})"
        out += f'<button class="demo-btn" style="background:{bgv};color:{fgv};border-radius:{rad}">{label}</button>'
    return out

# count derived
def count_derived(n):
    c = 0
    if isinstance(n, dict):
        if n.get("$extensions",{}).get("wise.derived"): c += 1
        for k,v in n.items():
            if not k.startswith("$"): c += count_derived(v)
    return c
N_DERIVED = count_derived(tokens)

# ============================================================
# NAV registry (drives sidebar + scroll-spy). Constant chassis order.
# ============================================================
NAV = [
    ("Overview",  [("overview","Dashboard")]),
    ("Foundation",[("color","Color"),("typography","Typography"),("iconography","Iconography"),
                   ("spacing","Spacing"),("radius","Radius"),("size","Size"),("grid","Grid"),
                   ("focus","Focus states"),("motion","Motion")]),
    ("Components",[("button","Button")]),
    ("System",    [("modules","Modules"),("support","Support")]),
]
GROUP_ICON = {"Overview":"◎","Foundation":"◳","Components":"◆","System":"⊞"}

def sidebar():
    groups = ""
    for gname, links in NAV:
        items = "".join(f'<a href="#{sid}" class="ds-nav-link">{esc(label)}</a>' for sid,label in links)
        groups += (f'<div class="ds-nav-group"><button class="ds-nav-label" aria-expanded="true" '
                   f'onclick="toggleNavGroup(this)"><span class="gi">{GROUP_ICON.get(gname,"•")}</span>'
                   f'<span>{esc(gname)}</span><span class="chev">⌄</span></button>'
                   f'<div class="ds-nav-list">{items}</div></div>')
    return groups

# ============================================================
# ASSEMBLE
# ============================================================
page = f"""<!doctype html><html lang="en" data-theme="light"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(DS_NAME)} — Reference</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root{{
  --space-2:8px;--space-3:12px;--space-4:16px;--space-6:24px;--space-8:32px;
  --nav-w:248px;--topbar-h:60px;
  --shadow-md:0 4px 14px rgba(0,0,0,.08);--shadow-lg:0 16px 40px rgba(0,0,0,.16);
{light_css}}}
{vars_block('[data-theme="dark"]', dark)}
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
html{{scroll-behavior:smooth}}
body{{font-family:var(--font-body);background:var(--surface-page);color:var(--text-primary);
  line-height:1.5;font-weight:500;-webkit-font-smoothing:antialiased;
  transition:background .25s,color .25s}}
a{{color:var(--text-link);text-decoration:none}}
code{{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.85em}}
.ds-shell{{display:flex;min-height:100vh}}
/* Sidebar */
.ds-sidebar{{width:var(--nav-w);flex-shrink:0;position:sticky;top:0;height:100vh;overflow-y:auto;
  background:var(--surface-elevated);border-right:1px solid var(--border-default);
  padding:var(--space-6);display:flex;flex-direction:column;gap:var(--space-6)}}
.ds-logo{{display:flex;align-items:center;gap:10px;font-family:var(--font-display);font-weight:600;font-size:18px}}
.ds-logo .dot{{width:26px;height:26px;border-radius:8px;background:var(--accent-bg);
  display:flex;align-items:center;justify-content:center;color:var(--accent-text);font-size:14px}}
.ds-nav-group{{display:flex;flex-direction:column}}
.ds-nav-label{{display:flex;align-items:center;gap:8px;background:none;border:none;cursor:pointer;
  font:inherit;font-size:12px;text-transform:uppercase;letter-spacing:.06em;color:var(--text-tertiary);
  padding:6px 4px;width:100%}}
.ds-nav-label .gi{{font-size:13px}}.ds-nav-label .chev{{margin-left:auto;transition:transform .2s}}
.ds-nav-label[aria-expanded="false"] .chev{{transform:rotate(-90deg)}}
.ds-nav-list{{display:flex;flex-direction:column;gap:1px;margin:4px 0 0}}
.ds-nav-label[aria-expanded="false"]+.ds-nav-list{{display:none}}
.ds-nav-link{{color:var(--text-secondary);padding:7px 10px;border-radius:8px;font-size:14px}}
.ds-nav-link:hover{{background:var(--surface-subtle);color:var(--text-primary)}}
.ds-nav-link.active{{background:var(--accent-bg);color:var(--accent-text);font-weight:600}}
/* Main */
.ds-main{{flex:1;min-width:0;display:flex;flex-direction:column}}
.ds-topbar{{position:sticky;top:0;z-index:20;height:var(--topbar-h);display:flex;align-items:center;
  gap:12px;padding:0 var(--space-8);background:var(--surface-page);border-bottom:1px solid var(--border-default)}}
.ds-topbar-title{{font-weight:600;font-size:15px}}
.ds-topbar-actions{{margin-left:auto;display:flex;gap:8px}}
.ds-iconbtn{{height:38px;padding:0 14px;border:1px solid var(--border-default);background:var(--surface-page);
  color:var(--text-secondary);border-radius:var(--radius-pill);cursor:pointer;font:inherit;font-size:13px;
  display:flex;align-items:center;gap:6px}}
.ds-iconbtn:hover{{background:var(--surface-subtle);color:var(--text-primary)}}
.ds-content{{max-width:1040px;width:100%;margin:0 auto;padding:var(--space-8)}}
section{{padding:36px 0;border-bottom:1px solid var(--border-default);scroll-margin-top:var(--topbar-h)}}
.eyebrow{{font-size:12px;text-transform:uppercase;letter-spacing:.08em;color:var(--text-tertiary);margin-bottom:6px}}
h2{{font-family:var(--font-display);font-size:30px;margin-bottom:6px}}
h3{{font-size:19px;margin:26px 0 8px}}
h4{{font-size:12px;text-transform:uppercase;letter-spacing:.05em;color:var(--text-tertiary);margin:20px 0 10px}}
p.lead{{color:var(--text-secondary);max-width:660px}}
.note{{background:var(--surface-subtle);border:1px solid var(--border-default);border-radius:12px;
  padding:12px 16px;font-size:14px;color:var(--text-secondary);margin:14px 0}}
.sw-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(270px,1fr));gap:14px}}
.sw{{display:flex;gap:12px}}.chip{{width:42px;height:42px;border-radius:10px;border:1px solid var(--border-default);flex:none}}
.sw code{{font-size:13px;font-weight:600}}.sw .v{{display:block;color:var(--text-tertiary);font-size:12px}}
.sw p{{font-size:12px;color:var(--text-tertiary);margin-top:2px}}
.d{{display:inline-block;background:var(--interactive-bg);color:var(--interactive-text);font-size:10px;
  padding:1px 6px;border-radius:6px;margin-left:6px;vertical-align:middle}}
table{{width:100%;border-collapse:collapse;font-size:14px;margin-top:8px}}
th,td{{text-align:left;padding:8px 10px;border-bottom:1px solid var(--border-default)}}
th{{color:var(--text-tertiary);font-weight:600;font-size:12px;text-transform:uppercase;letter-spacing:.04em}}
.typerow{{display:flex;justify-content:space-between;align-items:center;gap:24px;padding:14px 0;border-bottom:1px solid var(--border-default)}}
.typerow .sample{{flex:1;min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.typerow .meta{{font-size:12px;color:var(--text-tertiary);text-align:right;flex:none}}
/* Spacing visual bars (MAI spec) */
.space-row{{display:flex;align-items:center;gap:16px;margin-bottom:12px}}
.space-bar{{background:var(--accent-bg);height:8px;border-radius:4px;flex-shrink:0}}
.space-info{{font-size:13px;color:var(--text-secondary);font-family:ui-monospace,SFMono-Regular,Menlo,monospace}}
.space-intent{{color:var(--text-link);font-weight:600}}
/* Theme switch */
.ds-theme-switch{{display:flex;align-items:center;gap:10px;cursor:pointer;user-select:none;font-size:13px;color:var(--text-secondary)}}
.ds-switch-track{{width:46px;height:26px;border-radius:999px;background:var(--surface-subtle);border:1px solid var(--border-default);position:relative;transition:background .2s}}
.ds-switch-knob{{position:absolute;top:2px;left:2px;width:20px;height:20px;border-radius:50%;background:var(--accent-bg);color:var(--accent-text);display:flex;align-items:center;justify-content:center;font-size:12px;transition:left .2s}}
[data-theme="dark"] .ds-switch-knob{{left:22px}}
/* Support panel (MAI spec) */
.support-panel{{background:var(--surface-subtle);border:1px solid var(--border-default);border-radius:var(--radius-card);padding:40px;text-align:center;margin-top:14px}}
.support-panel-icon{{width:54px;height:54px;border-radius:50%;border:1.5px solid var(--text-link);display:inline-flex;align-items:center;justify-content:center;font-size:24px;color:var(--text-link);margin-bottom:14px}}
.support-panel-title{{font-family:var(--font-display);font-size:21px;margin-bottom:6px}}
.support-panel-desc{{color:var(--text-secondary);max-width:460px;margin:0 auto 20px;font-size:14px}}
.ds-dialog{{border:none;border-radius:var(--radius-card);padding:0;max-width:460px;width:92%;background:var(--surface-page);color:var(--text-primary);box-shadow:var(--shadow-lg)}}
.ds-dialog::backdrop{{background:rgba(0,0,0,.45)}}
.ds-dialog-card{{padding:26px}}
.ds-dialog-header{{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:18px}}
.ds-dialog-title{{font-family:var(--font-display);font-size:20px}}
.ds-dialog-sub{{font-size:13px;color:var(--text-tertiary);margin-top:2px}}
.ds-dialog-close{{background:none;border:none;font-size:24px;color:var(--text-tertiary);cursor:pointer;line-height:1}}
.form-row{{display:flex;gap:12px}}.form-row .form-group{{flex:1}}
.form-group{{margin-bottom:14px;display:flex;flex-direction:column}}
.form-label{{font-size:13px;font-weight:600;margin-bottom:5px}}
.form-input{{border:1px solid var(--border-default);border-radius:10px;padding:10px 12px;font:inherit;font-size:14px;background:var(--surface-page);color:var(--text-primary)}}
.form-input:focus{{outline:2px solid var(--focus-ring);outline-offset:1px;border-color:transparent}}
.form-counter{{font-size:12px;color:var(--text-tertiary);text-align:right;margin-top:4px}}
.ds-dialog-meta{{font-size:12px;color:var(--text-tertiary);background:var(--surface-subtle);border-radius:8px;padding:8px 10px;margin:6px 0 16px}}
.ds-dialog-footer{{display:flex;justify-content:flex-end;gap:10px}}
.form-success{{text-align:center;padding:14px 0}}
.form-success-icon{{font-size:38px;color:var(--sentiment-pos);margin-bottom:8px}}
.btn-secondary{{background:transparent;border:1px solid var(--border-default);color:var(--text-primary);border-radius:var(--radius-pill);padding:10px 20px;font:inherit;font-weight:600;cursor:pointer}}
.demo-btn{{border:none;padding:0 22px;height:48px;font-family:inherit;font-weight:600;font-size:15px;margin:6px 8px 6px 0;cursor:pointer}}
.demo-btn:focus-visible{{outline:2px solid var(--focus-ring);outline-offset:2px}}
.radii{{display:flex;gap:16px;flex-wrap:wrap}}
.radii div{{width:92px;height:92px;background:var(--accent-bg);color:var(--accent-text);display:flex;
  align-items:flex-end;justify-content:center;padding-bottom:6px;font-size:11px;font-weight:600;text-align:center}}
.principles{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}}
.principles div{{background:var(--surface-subtle);border-radius:12px;padding:16px;font-size:14px}}
.principles b{{display:block;margin-bottom:4px}}
/* Overview dashboard */
.ov-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:14px;margin-top:18px}}
.ov-card{{background:var(--surface-elevated);border:1px solid var(--border-default);border-radius:var(--radius-card);padding:18px}}
.ov-card .k{{font-size:12px;text-transform:uppercase;letter-spacing:.05em;color:var(--text-tertiary)}}
.ov-card .val{{font-size:20px;font-weight:600;margin-top:4px;word-break:break-word}}
.ov-card .val a{{font-size:14px}}
.stat-row{{display:flex;gap:14px;flex-wrap:wrap;margin-top:18px}}
.stat{{background:var(--accent-bg);color:var(--accent-text);border-radius:var(--radius-card);padding:16px 20px;min-width:120px}}
.stat .n{{font-size:28px;font-weight:700;font-family:var(--font-display)}}
.stat .l{{font-size:12px;opacity:.85}}
/* Module pattern */
.ds-module__card{{position:relative;background:var(--surface-subtle);border:1px solid var(--border-default);
  border-radius:var(--radius-card);padding:36px;text-align:center;margin-top:10px}}
.ds-module__icon{{width:52px;height:52px;border-radius:50%;border:1.5px solid var(--text-link);
  display:inline-flex;align-items:center;justify-content:center;font-size:22px;color:var(--text-link);margin-bottom:12px}}
.ds-module__subhead{{font-family:var(--font-display);font-size:20px;margin-bottom:6px}}
.ds-module__desc{{color:var(--text-secondary);max-width:440px;margin:0 auto 18px;font-size:14px}}
.pill{{border:1px solid var(--text-link);background:var(--interactive-bg);color:var(--interactive-text);
  border-radius:var(--radius-pill);padding:10px 22px;font:inherit;font-size:14px;font-weight:600;cursor:pointer}}
.pill--corner{{position:absolute;top:14px;right:14px;background:transparent;color:var(--text-link);padding:6px 14px}}
.pill--ghost{{background:transparent;color:var(--text-link)}}
.ds-module__stub{{display:none;align-items:center;justify-content:space-between;
  border:1px dashed var(--border-default);border-radius:var(--radius-pill);padding:10px 16px;margin-top:10px}}
.is-excluded .ds-module__card{{display:none}}
.is-excluded .ds-module__stub{{display:flex}}
/* Downloads modal */
.ds-modal{{position:fixed;inset:0;background:rgba(0,0,0,.45);display:none;align-items:center;justify-content:center;z-index:50}}
.ds-modal.open{{display:flex}}
.ds-modal-card{{background:var(--surface-page);border:1px solid var(--border-default);border-radius:var(--radius-card);
  padding:26px;max-width:420px;width:90%}}
.ds-modal-card h3{{margin:0 0 12px}}
.dl-row{{display:flex;justify-content:space-between;align-items:center;gap:12px;padding:10px 0;border-bottom:1px solid var(--border-default)}}
.dl-row:last-child{{border-bottom:none}}
@media(max-width:820px){{.ds-sidebar{{display:none}}.principles{{grid-template-columns:1fr}}.typerow{{flex-direction:column;align-items:flex-start;gap:8px}}.typerow .meta{{text-align:left}}}}
</style></head>
<body>
<div class="ds-shell">
  <nav class="ds-sidebar" aria-label="Design system navigation">
    <div class="ds-logo"><span class="dot">◆</span>{esc(DS_NAME)}</div>
    {sidebar()}
  </nav>
  <div class="ds-main">
    <header class="ds-topbar">
      <span class="ds-topbar-title">{esc(DS_NAME)} — {esc(PLATFORM.title())} Reference v{esc(VERSION)}</span>
      <div class="ds-topbar-actions">
        <button class="ds-iconbtn" onclick="openDownloads()">↓ Downloads</button>
        <div class="ds-theme-switch" role="switch" aria-checked="false" tabindex="0" onclick="toggleTheme()" onkeydown="if(event.key==='Enter'||event.key===' '){{event.preventDefault();toggleTheme();}}">
          <span id="themeLabel">Dark Theme</span>
          <span class="ds-switch-track"><span class="ds-switch-knob" id="themeKnob">☀</span></span>
        </div>
      </div>
    </header>
    <div class="ds-content">

    <section id="overview">
      <p class="eyebrow">Overview</p>
      <h2>{esc(DS_NAME)}</h2>
      <p class="lead">A complete, production-ready design system audited from the source and generated from a canonical <code>tokens.json</code>. This reference, the token file and the Figma import are all generated views of that single source of truth.</p>
      <div class="ov-grid">
        <div class="ov-card"><div class="k">Author</div><div class="val">{esc(AUTHOR)}</div></div>
        <div class="ov-card"><div class="k">Version</div><div class="val">v{esc(VERSION)}</div></div>
        <div class="ov-card"><div class="k">Platform</div><div class="val">{esc(PLATFORM.title())}</div></div>
        <div class="ov-card"><div class="k">Audited</div><div class="val">{esc(AUDITED)}</div></div>
        <div class="ov-card"><div class="k">Source</div><div class="val"><a href="{esc(SOURCE)}" target="_blank" rel="noopener">{esc(SOURCE.replace('https://','').rstrip('/'))}</a></div></div>
        <div class="ov-card"><div class="k">Structure</div><div class="val" style="font-size:14px">{esc(meta.get('structureModel','Material'))}</div></div>
      </div>
      <div class="stat-row">
        <div class="stat"><div class="n">2</div><div class="l">Themes (light / dark)</div></div>
        <div class="stat"><div class="n">{len([1 for g in NAV for _ in g[1]])}</div><div class="l">Reference sections</div></div>
        <div class="stat"><div class="n">{N_DERIVED}</div><div class="l">Derived placeholders</div></div>
      </div>
      <div class="note">⚠︎ Tokens tagged <span class="d">derived</span> are not published numerically by the source (dark-mode hex, type scale, motion timings, hover/active states). They follow the source's documented logic and are safe to replace with official values.</div>
    </section>

    <section id="color"><p class="eyebrow">Foundation</p><h2>Color</h2>
      <p class="lead">Semantic roles, named by intent. Light is audited; dark is derived.</p>
      <h3>Light theme</h3>{color_theme("light")}
      <h3>Dark theme <span class="d">derived</span></h3>{color_theme("dark")}
      <h3>Primitive palette</h3><h4>Core &amp; secondary</h4>{swatches({**P['color']['core'], **P['color']['secondary']})}
    </section>

    <section id="typography"><p class="eyebrow">Foundation</p><h2>Typography</h2>
      <p class="lead">{esc(FONT_BODY)} for product; {esc(FONT_DISPLAY)} for short display moments. Numeric scale is derived.</p>
      {type_rows()}
    </section>

    <section id="iconography"><p class="eyebrow">Foundation</p><h2>Iconography</h2>
      <p class="lead">Solid lines, simple shapes, square terminals — designed to pair with the type families. Default product size 24px.</p>
      <table><thead><tr><th>Context</th><th>Sizes</th></tr></thead><tbody>
      <tr><td>Product</td><td>16px, 24px, 32px</td></tr>
      <tr><td>Editorial</td><td>16px, 24px, 48px, 64px, 96px</td></tr>
      <tr><td>Interactive</td><td>Forest Green (interactive-primary) on neutral</td></tr>
      <tr><td>Informational</td><td>Content Primary on neutral</td></tr></tbody></table>
    </section>

    <section id="spacing"><p class="eyebrow">Foundation</p><h2>Spacing</h2>
      <p class="lead">A single scale on a 4px base unit, with intent labels where a step has a canonical layout role.</p>
      <div style="margin-top:18px">{space_bars()}</div>
      <h3>Semantic — horizontal</h3>{dim_table(S['spacing']['horizontal'])}
      <h3>Semantic — vertical</h3>{dim_table(S['spacing']['vertical'])}
      <h3>Padding</h3>{dim_table(S['padding'])}
    </section>

    <section id="radius"><p class="eyebrow">Foundation</p><h2>Radius</h2>
      <p class="lead">Desktop scale shown; a tighter mobile scale lives in the token file.</p>{radii_demo()}</section>

    <section id="size"><p class="eyebrow">Foundation</p><h2>Size</h2>
      <p class="lead">Component heights.</p>{dim_table(S['size'])}</section>

    <section id="grid"><p class="eyebrow">Foundation</p><h2>Grid</h2>
      <p class="lead">5 breakpoints; max width 1440px, then centred.</p>{grid_table()}</section>

    <section id="focus"><p class="eyebrow">Foundation</p><h2>Focus states</h2>
      <p class="lead">Shown on keyboard tab, not click. Goes beyond WCAG 2.2 focus appearance.</p>
      {dim_table({k:v for k,v in S['focus'].items() if isinstance(v,dict) and '$value' in v})}</section>

    <section id="motion"><p class="eyebrow">Foundation</p><h2>Motion</h2>
      <p class="lead">Principles audited; durations &amp; easing derived. Flash guard: ≤3 colour changes per second.</p>
      <div class="principles">
        <div><b>Snappy · 60%</b>Fast, satisfying, match-cut. Not erratic.</div>
        <div><b>Fluid · 30%</b>Organic, flowing, morphing. Not directionless.</div>
        <div><b>Intuitive · 10%</b>Natural pace, physical weight. Not mechanical.</div></div>
      <h3>Duration <span class="d">derived</span></h3>{dim_table(S['motion']['duration'])}</section>

    <section id="button"><p class="eyebrow">Components</p><h2>Button</h2>
      <p class="lead">Types: default, negative. Priorities: primary, secondary, secondary-neutral, tertiary. Sizes 32 / 40 / 48px.</p>
      <div>{button_demo()}</div>
      <p class="note">Full state coverage (hover / active / focus / disabled) for every priority and the negative type lives in <code>tokens.json → component.button</code>.</p></section>

    <section id="modules"><p class="eyebrow">System</p><h2>Modules</h2>
      <p class="lead">Optional design systems and section packs. Add a module to include it in this system and its export; remove it to exclude it — the definition stays in the library and can be re-added anytime.</p>
      <div class="ds-module" data-module="data-viz" data-included="false">
        <div class="ds-module__card">
          <button class="pill pill--corner" data-action="remove">Remove</button>
          <span class="ds-module__icon">▤</span>
          <h3 class="ds-module__subhead">Data Visualization Pack</h3>
          <p class="ds-module__desc">Charts, axes, legends and dataviz colour ramps tuned to this system. A starter add-on module.</p>
          <button class="pill" data-action="start">Get Started</button>
        </div>
        <div class="ds-module__stub"><span>Data Visualization Pack</span><button class="pill pill--ghost" data-action="add">Add</button></div>
      </div>
    </section>

    <section id="support" style="border-bottom:none"><p class="eyebrow">Support</p><h2>Feedback &amp; Enhancements</h2>
      <div class="support-panel">
        <div class="support-panel-icon">✎</div>
        <div class="support-panel-title">Help shape the system</div>
        <p class="support-panel-desc">To submit feedback or feature enhancements, email us. Your note goes straight to the design system admin.</p>
        <button class="pill" onclick="openFeedback()">✈ Send Feedback</button>
      </div>
    </section>

    </div>
  </div>
</div>

<dialog class="ds-dialog" id="feedback-dialog" aria-labelledby="feedback-title">
  <div class="ds-dialog-card">
    <form id="feedback-form" method="dialog" onsubmit="submitFeedback(event)">
      <div class="ds-dialog-header">
        <div>
          <div class="ds-dialog-title" id="feedback-title">Send Feedback</div>
          <div class="ds-dialog-sub">Feature requests, bugs, or ideas — all welcome.</div>
        </div>
        <button type="button" class="ds-dialog-close" aria-label="Close" onclick="closeFeedback()">&times;</button>
      </div>
      <div class="form-row">
        <div class="form-group"><label class="form-label" for="fb-first">First name</label>
          <input class="form-input" id="fb-first" name="first" type="text" required autocomplete="given-name"></div>
        <div class="form-group"><label class="form-label" for="fb-last">Last name</label>
          <input class="form-input" id="fb-last" name="last" type="text" required autocomplete="family-name"></div>
      </div>
      <div class="form-group"><label class="form-label" for="fb-email">Your email</label>
        <input class="form-input" id="fb-email" name="email" type="email" required autocomplete="email" placeholder="you@example.com"></div>
      <div class="form-group"><label class="form-label" for="fb-message">Feedback</label>
        <textarea class="form-input" id="fb-message" name="message" rows="4" maxlength="250" required
          placeholder="Share your feedback or feature request (250 characters max)" oninput="updateCounter()" style="resize:vertical"></textarea>
        <div class="form-counter"><span id="fb-count">0</span>/250</div>
      </div>
      <div class="ds-dialog-meta">Tagged automatically with date, time &amp; DS version on submit.</div>
      <div class="ds-dialog-footer">
        <button type="button" class="btn-secondary" onclick="closeFeedback()">Cancel</button>
        <button type="submit" class="pill">✈ Submit</button>
      </div>
    </form>
    <div class="form-success" id="feedback-success" style="display:none">
      <div class="form-success-icon">✓</div>
      <div class="ds-dialog-title" style="margin-bottom:8px">Thank you</div>
      <p class="support-panel-desc" style="margin-bottom:20px">Your email draft is ready to send. We appreciate you helping improve the system.</p>
      <button type="button" class="pill" onclick="closeFeedback()">Done</button>
    </div>
  </div>
</dialog>

<div class="ds-modal" id="dlModal" onclick="if(event.target===this)closeDownloads()">
  <div class="ds-modal-card">
    <h3>Downloads</h3>
    <div class="dl-row"><span>Canonical tokens (W3C)</span><a class="pill" href="tokens.json" download>tokens.json</a></div>
    <div class="dl-row"><span>Figma import (Tokens Studio)</span><a class="pill" href="figma-tokens.json" download>figma-tokens.json</a></div>
    <div class="dl-row"><span>Body font</span><a class="pill pill--ghost" href="https://fonts.google.com/specimen/Inter" target="_blank" rel="noopener">{esc(FONT_BODY)} ↗</a></div>
    <div class="dl-row"><span>Display font</span><span style="color:var(--text-tertiary);font-size:13px">{esc(FONT_DISPLAY)} (brand-licensed)</span></div>
    <div style="text-align:right;margin-top:16px"><button class="ds-iconbtn" onclick="closeDownloads()">Close</button></div>
  </div>
</div>

<script>
function syncTheme(){{
  var dark=document.documentElement.getAttribute('data-theme')==='dark';
  document.getElementById('themeLabel').textContent=dark?'Light Theme':'Dark Theme';
  document.getElementById('themeKnob').textContent=dark?'☾':'☀';
  var sw=document.querySelector('.ds-theme-switch'); if(sw)sw.setAttribute('aria-checked',dark);
}}
function toggleTheme(){{
  var r=document.documentElement;
  r.setAttribute('data-theme', r.getAttribute('data-theme')==='dark'?'light':'dark');
  syncTheme();
}}
syncTheme();
function toggleNavGroup(btn){{
  btn.setAttribute('aria-expanded', btn.getAttribute('aria-expanded')==='true'?'false':'true');
}}
function openDownloads(){{document.getElementById('dlModal').classList.add('open');}}
function closeDownloads(){{document.getElementById('dlModal').classList.remove('open');}}
// Scroll-spy: highlight active nav link
var links=[].slice.call(document.querySelectorAll('.ds-nav-link'));
var secs=links.map(function(l){{return document.querySelector(l.getAttribute('href'));}});
var spy=new IntersectionObserver(function(es){{
  es.forEach(function(e){{
    if(e.isIntersecting){{
      links.forEach(function(l){{l.classList.remove('active');}});
      var i=secs.indexOf(e.target);
      if(i>-1)links[i].classList.add('active');
    }}
  }});
}},{{rootMargin:'-55px 0px -75% 0px'}});
secs.forEach(function(s){{if(s)spy.observe(s);}});
// Module add/remove (data-included drives export inclusion)
document.querySelectorAll('.ds-module').forEach(function(m){{
  function set(on){{m.dataset.included=on?'true':'false';m.classList.toggle('is-excluded',!on);}}
  set(m.dataset.included==='true');
  var rm=m.querySelector('[data-action="remove"]'),ad=m.querySelector('[data-action="add"]'),
      st=m.querySelector('[data-action="start"]');
  if(rm)rm.onclick=function(){{set(false);}};
  if(ad)ad.onclick=function(){{set(true);}};
  if(st)st.onclick=function(){{set(true);alert('Get Started: opens module setup (platform + notes), then emits a scoped prompt for Claude to author the module and append it to the section library.');}};
}});
// Feedback dialog
var DS_VERSION="{esc(VERSION)}", ADMIN_EMAIL="{esc(ADMIN_EMAIL)}", DS_LABEL="{esc(DS_NAME)} v{esc(VERSION)}";
var fbDlg=document.getElementById('feedback-dialog');
function openFeedback(){{document.getElementById('feedback-success').style.display='none';
  document.getElementById('feedback-form').style.display='block';
  if(fbDlg.showModal)fbDlg.showModal();else fbDlg.setAttribute('open','');}}
function closeFeedback(){{if(fbDlg.close)fbDlg.close();else fbDlg.removeAttribute('open');}}
function updateCounter(){{document.getElementById('fb-count').textContent=document.getElementById('fb-message').value.length;}}
function submitFeedback(e){{e.preventDefault();
  var f=document.getElementById('fb-first').value,l=document.getElementById('fb-last').value,
      em=document.getElementById('fb-email').value,msg=document.getElementById('fb-message').value,
      stamp=new Date().toLocaleString();
  var body=encodeURIComponent(msg+"\\n\\n— "+f+" "+l+" ("+em+")\\n"+DS_LABEL+" · "+stamp);
  var subj=encodeURIComponent("["+DS_LABEL+"] Feedback from "+f+" "+l);
  if(ADMIN_EMAIL)window.location.href="mailto:"+ADMIN_EMAIL+"?subject="+subj+"&body="+body;
  document.getElementById('feedback-form').style.display='none';
  document.getElementById('feedback-success').style.display='block';
}}
</script>
</body></html>"""

open(ROOT / "reference.html", "w").write(page)
print("wrote reference.html", len(page), "bytes")
