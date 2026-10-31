# Contributing
>We highly recommend usage of our tooling. (documented down below)
## Scope

- `scripts/<name>/`: standalone tools that talk to SwayFX over the IPC socket.
- `patches/<name>/`: changes to SwayFX source, one directory per feature, no cross-dependencies between patches.
- `configs/`, `docs/`: examples and documentation.

Features that fit upstream should go to SwayFX directly.

## Requirements for every tool or patch

1. A directory named after the tool, containing:
   - `manifest.toml`
   - `README.md` (what it does, how to install or apply, known limits)
   - Sources, or `NNNN-*.patch` files created with `git format-patch`
2. A named maintainer (GitHub handle) in `manifest.toml` and in `.github/CODEOWNERS`.
3. A license: MIT by default. Another license needs an SPDX header in each file or a `REUSE.toml` in the tool directory.
4. No cross-dependencies on other tools in this repository.
5. Tested against the SwayFX version recorded in `swayfx_tested`.
6. No code comments, no generated or vendored binaries.
7. Every commit carries a `Signed-off-by` line (`git commit -s`). This is the DCO, no CLA is required.

## manifest.toml

```toml
name = "example"
description = "One line summary."
maintainer = "github-handle"
swayfx_tested = "v0.0.0"
status = "active"
language = "python"
dependencies = ["python3"]
```

- `status`: `active` or `unmaintained`.
- `language` and `dependencies` (a list, may be empty): required for scripts, optional for patches.
- `swayfx_tested`: a SwayFX tag or commit.

## Patches

- Generate with `git format-patch` against a SwayFX tag.
- The series must apply with `git am --3way` onto `swayfx_tested`.
- Name files `0001-*.patch`, `0002-*.patch`, in order.

## Local setup

Enable the repository hook once per clone. It regenerates and stages the README index on every commit:

```
git config core.hooksPath .githooks
```

Requires Python 3.11 or newer. Never edit the table between the index markers by hand.

## Tooling

`tools/contrib` creates tools in the correct structure, puts them on their own branch, and helps open the pull request. It needs Python 3.11 or newer and git. `origin` must be a repository you can push to, normally your fork.

```
tools/contrib
tools/contrib create-patch <patch files or directory>
tools/contrib create-script <file or directory>
tools/contrib update-patch <name> <patch files or directory>
tools/contrib adopt <name>
tools/contrib change
tools/contrib apply-patch <name>...
tools/contrib list
```

- Without arguments (or as `tools/contrib pr`) it shows a menu of pull request presets: new patch, new script, update a patch, adopt a tool, other change. Each preset asks for what it needs and fills in the matching PR template.
- `change` is the "other change" preset: it commits what you edited in the working tree (docs, configs, workflows, tooling) on a new branch and offers to open the PR. `--title`, `--summary`, `--branch`, and `--yes` skip the questions.
- `create-patch` and `create-script` ask for name, description, maintainer, SwayFX version (and language and dependencies for scripts), each on its own line. Every answer can also be passed as an option, for example `--name` or `--description`.
- They create `patches/<name>` or `scripts/<name>` with `manifest.toml` and `README.md`, add the `CODEOWNERS` entry, regenerate and validate the index, and commit with a sign-off on a new branch (`add-patch/<name>`, `add-script/<name>`). Then they offer to push and open the pull request, with the template already filled in. Use `--push` to skip the question and `--no-git` to only write files.
- Patches must be made with `git format-patch` from signed-off commits. `create-patch` checks this and verifies that the series applies on the SwayFX version you name. Use `--no-verify` to skip the apply check.
- `update-patch` replaces the patch files of your tool and the tested version, on a branch `update-patch/<name>`.
- `adopt` makes you the maintainer of an unmaintained tool, on a branch `adopt/<name>`.
- `apply-patch` clones SwayFX, checks out the version the patch was tested on, and applies it on a branch `contrib/<name>`. `--base latest`, `--base head`, or `--base <ref>` selects another version, and `--dir` sets the target. If it does not apply, nothing is left behind.
- The maintainer default comes from `git config github.user`. Set `SWAYFX_UPSTREAM` to use another SwayFX repository.

## Pull requests

- New tools and patches always get human review.
- The maintainer of a tool can change their own directory without review. A workflow approves and auto-merges a PR when all changed files lie inside directories whose maintainer (read from the base branch) is the PR author and all required checks pass.
- Anything else needs review: changes to `manifest.toml`, to another maintainer's directory, or to files outside `patches/<name>/` and `scripts/<name>/`.
- Changing the maintainer of a tool is done by a PR that also edits `manifest.toml` and `.github/CODEOWNERS`. The previous maintainer or a repository owner must approve it, unless the tool is unmaintained.

## Bot labels

When a PR cannot be auto-merged, the bot comments with the reasons and applies labels:

- `NEW`: adds a new patch or script
- `nCO`: changes files outside a single tool directory (not content)
- `nAUTH`: the author is not the maintainer of the touched tool
- `MANIFEST`: changes a `manifest.toml`

Labels and the comment are updated on every push. If the PR later qualifies, the labels are removed and auto-merge is enabled.

## Required checks

- `reuse`: license compliance
- `validate`: manifests, CODEOWNERS entries, README index
- `shellcheck`: shell scripts
- `patch-apply`: touched patches apply on the latest SwayFX tag and the default branch

## Lifecycle

1. The scheduled job finds a patch that no longer applies and opens an issue naming the maintainer.
2. After 60 days without a fix, a repository owner sets `status = "unmaintained"`.
3. After a further 120 days, the tool is deleted. Git history keeps it.
4. Anyone can adopt an unmaintained tool by opening a PR that sets themselves as maintainer.

The time windows are a proposal and can be changed here.

## Conduct

Be direct and respectful. Reviews address code, not people.
