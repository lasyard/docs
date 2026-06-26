# ![lasydoc](_images/lasydoc.png)

[![Documentation Status](https://readthedocs.org/projects/lasy/badge/?version=latest)](https://lasy.readthedocs.io/?badge=latest)

This project contains documentation work of mine. It is a Sphinx documentation project rooted at `index.md`.

## Build and validation commands

Build or valdition:

```sh
lasphinx/build.sh
```

To clean the generated files:

```sh
make clean
```

Do not use `lasphinx/build.sh clean`, it would delete files which are part of sources.

`Makefile` is the standard Sphinx passthrough makefile, so additional Sphinx targets such as `make help`, `make linkcheck`, `make singlehtml`, and `make doctest` are exposed by Sphinx.

## High-level architecture

- Navigation is driven by MyST `toctree` directives in `index.md` and each section's own `index.md`
- Most sections use `:glob:` so adding or renaming pages does not require to modify the `index.md`
- `conf.py` is the authoritative Sphinx configuration. It import `lasphinx`, which enables MyST, `sphinx-copybutton`, `sphinx-design`, `sphinx_rtd_theme`, `sphinxcontrib.mermaid`, and loads local extensions in `lasphinx/ext`

Special underscore-prefixed directories:

| Directory            | Purpose                                                                                                |
| -------------------- | ------------------------------------------------------------------------------------------------------ |
| `_files/`            | stores source snippets, configs, manifests, and command outputs that pages embed with `literalinclude` |
| `_generated_images/` | stores generated PNG assets referenced from Markdown pages, which are also part of sources             |
| `_images/`           | holds source images, including `.drawio` and `.puml` inputs for generated diagrams                     |

`.readthedocs.yaml` is the configuration for auto building in website `readthedocs.io`, don't touch it.

MIT License: <https://lasy.fwh.is/mit_license>.
