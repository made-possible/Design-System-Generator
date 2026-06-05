#!/usr/bin/env python3
"""Generate a Figma-importable token set (Tokens Studio format) from tokens.json.
Spoke of the canonical hub. Import via the Tokens Studio for Figma plugin ->
Tools -> Import -> figma-tokens.json, then "Create variables".
Run: python3 build_figma.py"""
import json, pathlib

ROOT = pathlib.Path(__file__).parent
src = json.load(open(ROOT / "tokens.json"))

# Tokens Studio type mapping from W3C $type
TYPE_MAP = {
    "color": "color", "dimension": "sizing", "duration": "other",
    "cubicBezier": "other", "fontFamily": "fontFamilies",
    "fontWeight": "fontWeights", "typography": "typography",
}

def convert(node):
    """Recursively convert a W3C token tree into Tokens Studio shape."""
    if isinstance(node, dict) and "$value" in node:
        t = node.get("$type", "other")
        out = {"value": node["$value"], "type": TYPE_MAP.get(t, "other")}
        if "$description" in node:
            out["description"] = node["$description"]
        return out
    out = {}
    for k, v in node.items():
        if k.startswith("$"):
            continue
        if isinstance(v, dict):
            out[k] = convert(v)
    return out

# Tokens Studio resolves references as {group.name} without the $ — our refs already match.
figma = {
    "primitive": convert(src["primitive"]),
    "semantic": convert(src["semantic"]),
    "component": convert(src["component"]),
    "$themes": [],
    "$metadata": {"tokenSetOrder": ["primitive", "semantic", "component"]},
}

out = ROOT / "figma-tokens.json"
json.dump(figma, open(out, "w"), indent=2)
print("wrote figma-tokens.json")
