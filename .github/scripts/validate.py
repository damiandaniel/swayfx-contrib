import sys
import tomllib
from pathlib import Path

KINDS = {"patches": "patch", "scripts": "script"}
REQUIRED = ["name", "description", "maintainer", "swayfx_tested", "status"]
SCRIPT_REQUIRED = ["language", "dependencies"]
STATUSES = {"active", "unmaintained"}

errors = []
owners = Path(".github/CODEOWNERS").read_text().splitlines()

for parent, kind in KINDS.items():
    base = Path(parent)
    for d in sorted(p for p in base.iterdir() if p.is_dir()):
        manifest = d / "manifest.toml"
        if not manifest.is_file():
            errors.append(f"{d}: missing manifest.toml")
            continue
        try:
            data = tomllib.loads(manifest.read_text())
        except tomllib.TOMLDecodeError as e:
            errors.append(f"{manifest}: {e}")
            continue
        required = REQUIRED + (SCRIPT_REQUIRED if kind == "script" else [])
        for key in required:
            if not data.get(key):
                errors.append(f"{manifest}: missing field {key}")
        if data.get("name") != d.name:
            errors.append(f"{manifest}: name must equal directory name")
        if data.get("status") not in STATUSES:
            errors.append(f"{manifest}: status must be one of {sorted(STATUSES)}")
        if not (d / "README.md").is_file():
            errors.append(f"{d}: missing README.md")
        if kind == "patch" and not list(d.glob("*.patch")):
            errors.append(f"{d}: no .patch files")
        maintainer = data.get("maintainer", "")
        prefix = f"/{parent}/{d.name}/"
        entry = [l.split() for l in owners if l.startswith(prefix + " ") or l.startswith(prefix + "\t")]
        if not entry or f"@{maintainer}" not in entry[-1][1:]:
            errors.append(f"CODEOWNERS: {prefix} must list @{maintainer}")

for e in errors:
    print(e)
sys.exit(1 if errors else 0)
