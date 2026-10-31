import sys
import tomllib
from pathlib import Path

START = "<!-- index:start -->"
END = "<!-- index:end -->"

rows = []
for parent in ("scripts", "patches"):
    for d in sorted(p for p in Path(parent).iterdir() if p.is_dir()):
        m = d / "manifest.toml"
        if not m.is_file():
            continue
        data = tomllib.loads(m.read_text())
        rows.append(
            f"| [{data['name']}]({parent}/{d.name}) | {parent[:-1]} | {data['description']} "
            f"| @{data['maintainer']} | {data['swayfx_tested']} | {data['status']} |"
        )

if rows:
    table = ["| Name | Type | Description | Maintainer | Tested on | Status |", "| --- | --- | --- | --- | --- | --- |"] + rows
else:
    table = ["No entries yet."]

readme = Path("README.md")
text = readme.read_text()
head, rest = text.split(START, 1)
_, tail = rest.split(END, 1)
new = head + START + "\n" + "\n".join(table) + "\n" + END + tail

if "--check" in sys.argv:
    sys.exit(0 if new == text else 1)
readme.write_text(new)
