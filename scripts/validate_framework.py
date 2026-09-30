"""Check portable metadata, roster coverage and local Markdown links.

Standard library only. This is a document-contract check, not a host-runtime,
full YAML-schema, engine capability or gameplay validation.
"""
from pathlib import Path
import re
import sys
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]


def validate(root):
    errors = []
    roles = sorted((root / "agents").glob("*.md"))
    skills = sorted((root / "skills").glob("*/SKILL.md"))
    for path in roles + skills:
        text = path.read_text(encoding="utf-8")
        front = re.match(r"\A---\s*\n(.*?)\n---(?:\s*\n|$)", text, re.S)
        if not front:
            errors.append(f"{path.relative_to(root)}: missing frontmatter")
            continue
        fields = front.group(1)
        expected = path.stem if path.parent.name == "agents" else path.parent.name
        name = re.search(r"^name:\s*['\"]?([a-z0-9-]+)['\"]?\s*$", fields, re.M)
        if not name or name.group(1) != expected:
            errors.append(f"{path.relative_to(root)}: role/skill name must match path")
        if not re.search(r"^description:\s*\S", fields, re.M):
            errors.append(f"{path.relative_to(root)}: missing description")
        if re.search(r"^(model|memory|tools|permissionMode):", fields, re.M):
            errors.append(f"{path.relative_to(root)}: host metadata belongs in adapter")

    roster = (root / "ROSTER.md").read_text(encoding="utf-8")
    for name in re.findall(r"^\| `([a-z0-9-]+)` \|", roster, re.M):
        if not (root / "agents" / f"{name}.md").is_file():
            errors.append(f"ROSTER.md: missing agent {name}")

    links = 0
    for path in root.rglob("*.md"):
        if ".git" in path.relative_to(root).parts:
            continue
        text = path.read_text(encoding="utf-8")
        for match in re.finditer(r"\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)", text):
            target = match.group(1).strip("<>")
            if re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith("#"):
                continue
            target = unquote(target.split("#", 1)[0])
            if not target:
                continue
            links += 1
            if not (path.parent / target).exists():
                errors.append(f"{path.relative_to(root)}: missing link {target}")
    return errors, len(roles), len(skills), links


if __name__ == "__main__":
    errors, roles, skills, links = validate(ROOT)
    if errors:
        print("\n".join(errors))
        sys.exit(1)
    print(f"PASS: {roles} roles, {skills} skills, {links} local links")
    print("Document contracts only; live host/editor/gameplay validation is separate.")
