# Instructions for AI Agents

## Code of conduct

- Do not read/write files in the projects where Agents is not enabled (no `AGENTS.md` in the project root directory)
- Do not read/write files in other projects if you are working in one project, except being told so explicitly
- Do not read/write files that are being ignored by `git`, except being told so explicitly, or try to get my permission
- Refer to file `README.md`/`README.txt` if there is any
- If there are any inconsistencies between this doc and the real project status, stop the current working and request a confirmation; You can go on according the real project status if I confirmed

See `lasphinx/markdown.md` for coding conventions.

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

- This repository is a Sphinx documentation project rooted at `index.md`
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
