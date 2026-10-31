# swayfx-contrib

Community-maintained patches, scripts, and configs for SwayFX that are not suited for upstream.

This repository is not covered by upstream support. Report problems here, not in the SwayFX issue tracker.

## Layout

| Path | Content |
| --- | --- |
| `scripts/<name>/` | External tools (IPC scripts, helpers). No SwayFX source needed. |
| `patches/<name>/` | Compositor patch series against SwayFX. |
| `configs/` | Example configuration snippets. |
| `docs/` | Guides and policies. |
| `packaging/` | Package recipes, added on demand. |

## Index

<!-- index:start -->
| Name | Type | Description | Maintainer | Tested on | Status |
| --- | --- | --- | --- | --- | --- |
| [test-patch](patches/test-patch) | patche | Dummy patch for testing the repository automation. | @damiandaniel | 0.6 | active |
<!-- index:end -->

## Using a patch

```
git clone https://github.com/wlrfx/swayfx && cd swayfx
git checkout <tag from the patch manifest>
git am --3way /path/to/swayfx-contrib/patches/<name>/*.patch
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT by default. Individual tools may declare another license, see [REUSE](https://reuse.software) annotations.
