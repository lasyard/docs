# Copilot instructions for this repository

## Build and validation commands

```sh
pip install -r requirements.txt
make html
make clean
```

If a page depends on generated diagrams, build those before `make html`:

```sh
sphinx-common/scripts/build.sh
sphinx-common/scripts/build.sh clean
```

`Makefile` is the standard Sphinx passthrough makefile, so additional Sphinx targets such as `make help`, `make linkcheck`, `make singlehtml`, and `make doctest` are exposed by Sphinx.

There is no separate repo-local lint suite configured in the top-level `Makefile`, GitHub workflows, or checked-in tool configs. There is also no repo-specific single-test runner beyond the generic Sphinx targets above, so the normal verification path is a Sphinx build.

## High-level architecture

- This repository is a Sphinx documentation project rooted at `index.md`, with major topic areas split into top-level directories such as `app/`, `service/`, `os/`, `cluster/`, `bigdata/`, `devel/`, `ai/`, `notes/`, `maths/`, `physics/`, and `hardware/`.
- Navigation is driven by MyST `toctree` directives in `index.md` and each section's own `index.md`. Most sections use `:glob:` so adding or renaming pages often only requires updating the local section index, not a central manifest.
- `conf.py` is the authoritative Sphinx configuration. It enables MyST, `sphinx-copybutton`, `sphinx-design`, `sphinx_rtd_theme`, and `sphinxcontrib.mermaid`, and it loads two local extensions from `sphinx-common/ext`.
- `sphinx-common` is a git submodule that provides shared Sphinx extensions, styles, and asset-generation scripts. Read the local `sphinx-common/README.md` before changing extension behavior or image-generation workflow.
- Dotfiles, underscore-prefixed paths, and `sphinx-common` are excluded from Sphinx parsing via `exclude_patterns`, so underscore-prefixed directories are support assets rather than standalone documentation trees.
- `_files/` stores source snippets, configs, manifests, and command outputs that pages embed with `literalinclude`. `_generated_images/` stores generated PNG assets referenced from Markdown pages. `_images/` holds source images, including `.drawio` and `.puml` inputs for generated diagrams.
- `.readthedocs.yaml` installs `requirements.txt`, points Read the Docs at `conf.py`, and explicitly includes the `sphinx-common` submodule, so changes to shared extensions or assets affect both local and hosted builds.

## Key conventions

- Write docs in MyST Markdown, not reStructuredText. Existing pages use MyST fenced directives such as `:::{toctree}`, `:::{literalinclude}`, and admonitions like `:::{tip}`.
- New content pages typically live beside a section `index.md`; keep support material in `_files/`, `_images/`, or `_generated_images/` rather than mixing it into navigated content directories.
- When showing real configs, manifests, or console captures, prefer `literalinclude` from `_files/...` instead of pasting large inline code blocks. Many pages pair that with `:diff:` to show how a file changed from an original baseline.
- The repo overrides Sphinx's standard `literalinclude` directive in `sphinx-common/ext/lasyard_literalinclude.py`. That override auto-detects the language from the included file extension and strips diff headers when `:diff:` is used, so keep using `literalinclude` rather than working around syntax-highlighting or diff-header issues manually.
- Console examples frequently use ```console fences. The `ellipsis_to_vertical` extension rewrites standalone `...` lines inside console blocks, so preserve that style when abbreviating long terminal output.
- Image references are commonly root-relative (for example `/_generated_images/...` and `/_images/...`), and `literalinclude` targets are also commonly written with leading `/` paths relative to the docs source root.
- Section indexes often use `:glob:` and sometimes `:numbered:`. Preserve the existing local pattern when adding a page to a section instead of normalizing all indexes to one style.
- Follow `.editorconfig`: default indentation is 4 spaces, JSON/YAML use 2 spaces, Markdown keeps trailing whitespace, and `Makefile`/`.mk` files use tabs.
