# pandoc

<https://pandoc.org/>

## Install

::::{tab-set}
:::{tab-item} macOS Monterey

```console
$ brew install pandoc
```

Check the version:

```console
$ pandoc --version
pandoc 3.3
Features: +server +lua
Scripting engine: Lua 5.4
User data directory: /Users/xxxx/.local/share/pandoc
Copyright (C) 2006-2024 John MacFarlane. Web: https://pandoc.org
This is free software; see the source for copying conditions. There is no
warranty, not even for merchantability or fitness for a particular purpose.
```

:::
::::

To get the latest version, download installer packages from the official website.

## Usage

Convert `docx` to `md`:

```console
pandoc xxxx.docx -f docx -t markdown -o xxxx.md
```

List supported input formats:

```console
$ pandoc --list-input-formats
biblatex
bibtex
bits
commonmark
commonmark_x
creole
csljson
csv
djot
docbook
docx
dokuwiki
endnotexml
epub
fb2
gfm
haddock
html
ipynb
jats
jira
json
latex
man
markdown
markdown_github
markdown_mmd
markdown_phpextra
markdown_strict
mdoc
mediawiki
muse
native
odt
opml
org
pod
ris
rst
rtf
t2t
textile
tikiwiki
tsv
twiki
typst
vimwiki
```

No `pdf` support.

List supported output formats:

```console
$ pandoc --list-output-formats
ansi
asciidoc
asciidoc_legacy
asciidoctor
beamer
biblatex
bibtex
chunkedhtml
commonmark
commonmark_x
context
csljson
djot
docbook
docbook4
docbook5
docx
dokuwiki
dzslides
epub
epub2
epub3
fb2
gfm
haddock
html
html4
html5
icml
ipynb
jats
jats_archiving
jats_articleauthoring
jats_publishing
jira
json
latex
man
markdown
markdown_github
markdown_mmd
markdown_phpextra
markdown_strict
markua
mediawiki
ms
muse
native
odt
opendocument
opml
org
pdf
plain
pptx
revealjs
rst
rtf
s5
slideous
slidy
tei
texinfo
textile
typst
xwiki
zimwiki
```

Does support `pdf`.
