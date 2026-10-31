# swayfx-contrib

Community-maintained patches, scripts, and configs for SwayFX that are not suited for upstream.

This repository is not covered by upstream support. Report problems here, not in the SwayFX issue tracker.

## Layout

| Path | Content |
| --- | --- |
| `scripts/<name>/` | External tools (IPC scripts, helpers). No SwayFX source needed. |
| `patches/<name>/` | Compositor patch series against SwayFX. |
| `tools/` | The `contrib` command: create and update tools, open pull requests, apply patches. |
| `configs/` | Example configuration snippets. |
| `docs/` | Guides and policies. |
| `packaging/` | Package recipes, added on demand. |

## Index

<!-- index:start -->
No entries yet.
<!-- index:end -->

## Using a patch

This clones SwayFX, checks out the version the patch was tested on, and applies it on a new branch:

```
tools/contrib apply-patch <name>
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT by default. Individual tools may declare another license, see [REUSE](https://reuse.software) annotations.
