"""Spec Ghost — deterministic Kiro spec coverage scanner.

Fresh code, written 3 Nov 2026 for Kiroween 2026. No reuse of any
existing project. No LLM, no network, no GitHub API: every result is
computed from files on disk, so every result can be re-checked by
reading those files.

Concepts (haunted-house language is UI only; the logic is plain):
- A "spec" is a directory under <root>/.kiro/specs/<name>/, or a
  single .md file directly under <root>/.kiro/specs/.
- A spec is "covered" if at least one code file references it.
- A spec referenced by no code file is a "ghost" (orphan spec).
- A code file referencing no spec is "unmarked" (code with no spec).
- A spec is "stale" if it mentions a file path that no longer
  exists under <root>.

A code file references a spec when its text contains, case-insensitively,
the spec name (hyphens and underscores treated as equivalent), or an
explicit marker such as "spec: <name>" or ".kiro/specs/<name>".
"""
import os
import re

CODE_EXTS = {".py", ".js", ".ts", ".tsx", ".jsx", ".html", ".css", ".json"}
SKIP_DIRS = {".git", "__pycache__", "node_modules", ".venv", "venv", "runs"}

# A plausible file path mentioned in spec prose, e.g. app/server.py
PATH_RE = re.compile(r"`?([A-Za-z0-9_.\-/]+\.(?:py|js|ts|tsx|jsx|html|css|json|md))`?")


def _norm(name):
    return re.sub(r"[-_]+", "-", name.strip().lower())


def discover_specs(root):
    """Return {spec_name: {dir, files: [rel md paths], text}}."""
    specs_dir = os.path.join(root, ".kiro", "specs")
    specs = {}
    if not os.path.isdir(specs_dir):
        return specs
    for entry in sorted(os.listdir(specs_dir)):
        full = os.path.join(specs_dir, entry)
        if os.path.isdir(full):
            md_files = []
            text_parts = []
            for dirpath, dirnames, filenames in os.walk(full):
                dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
                for fn in sorted(filenames):
                    if fn.endswith(".md"):
                        rel = os.path.relpath(os.path.join(dirpath, fn), root)
                        md_files.append(rel)
                        with open(os.path.join(dirpath, fn), encoding="utf-8", errors="ignore") as f:
                            text_parts.append(f.read())
            if md_files:
                specs[entry] = {"dir": os.path.relpath(full, root), "files": md_files, "text": "\n".join(text_parts)}
        elif entry.endswith(".md"):
            with open(full, encoding="utf-8", errors="ignore") as f:
                text = f.read()
            specs[entry[:-3]] = {"dir": os.path.relpath(specs_dir, root), "files": [os.path.relpath(full, root)], "text": text}
    return specs


def discover_code_files(root):
    """Return [rel paths] of code files, excluding .kiro specs themselves."""
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not (dirpath == root and d == ".kiro")]
        for fn in sorted(filenames):
            if os.path.splitext(fn)[1] in CODE_EXTS:
                out.append(os.path.relpath(os.path.join(dirpath, fn), root))
    return out


def mentioned_files(spec_text):
    """File paths mentioned in a spec, normalised, de-duplicated."""
    found = []
    for m in PATH_RE.finditer(spec_text):
        p = m.group(1).strip("./")
        if p and p not in found:
            found.append(p)
    return found


def spec_referenced_by(spec_name, code_text):
    hay = _norm(code_text)
    needle = _norm(spec_name)
    if needle in hay:
        return True
    # Explicit marker forms, e.g. "spec: room-lighting"
    return f"spec: {needle}" in hay or f".kiro/specs/{needle}" in hay


def scan(root):
    """Scan root. Returns a JSON-serialisable report dict."""
    root = os.path.abspath(root)
    specs = discover_specs(root)
    code_files = discover_code_files(root)
    code_texts = {}
    for rel in code_files:
        with open(os.path.join(root, rel), encoding="utf-8", errors="ignore") as f:
            code_texts[rel] = f.read()

    covered, ghosts, stale = [], [], []
    spec_to_code = {}
    for name, spec in sorted(specs.items()):
        refs = [rel for rel in code_files if spec_referenced_by(name, code_texts[rel])]
        spec_to_code[name] = refs
        if refs:
            covered.append(name)
        else:
            ghosts.append(name)
        missing = [p for p in mentioned_files(spec["text"]) if not os.path.exists(os.path.join(root, p))]
        # Only count a mention as stale if it looks like a project path
        # (contains a slash or is a known code file), to avoid flagging
        # prose words like "README.md" mentioned generically without a path.
        missing = [p for p in missing if "/" in p]
        if missing:
            stale.append({"spec": name, "missing_files": missing})

    unmarked = []
    for rel in code_files:
        if not any(spec_referenced_by(name, code_texts[rel]) for name in specs):
            unmarked.append(rel)

    return {
        "root": root,
        "spec_count": len(specs),
        "code_file_count": len(code_files),
        "covered_specs": covered,
        "ghost_specs": ghosts,
        "unmarked_code_files": unmarked,
        "stale_specs": stale,
        "spec_to_code": spec_to_code,
        "specs": {name: {"dir": s["dir"], "files": s["files"], "mentioned_files": mentioned_files(s["text"])} for name, s in specs.items()},
    }


def banish_plan(ghost_name, report):
    """A PLAN ONLY. Never deletes files. Approval first, always.

    Returns a human-readable plan for what a human could do about a
    ghost spec: archive it, implement it, or delete it by hand.
    This function never touches the filesystem.
    """
    if ghost_name not in report.get("ghost_specs", []):
        return {"ghost": ghost_name, "plan": "Not a ghost spec in this report — nothing to banish.", "actions": [], "deletes_anything": False}
    spec = report["specs"][ghost_name]
    actions = [
        f"1. Read {', '.join(spec['files'])} and decide: is this spec still wanted?",
        "2. If YES: implement it, and add a 'spec: " + ghost_name + "' reference in the new code file, then re-run Spec Ghost.",
        "3. If NO: move the spec directory to an archive folder BY HAND (Spec Ghost never moves or deletes files).",
        "4. If UNSURE: leave it — a ghost is a question, not a bug. Re-run after the next change.",
    ]
    return {"ghost": ghost_name, "plan": "Banish plan (plan only — no files were changed).", "actions": actions, "deletes_anything": False}
